import inspect
import json
import unittest
from types import SimpleNamespace
from unittest import mock

from bs4 import BeautifulSoup

from glassdoorcrawler import cli
from glassdoorcrawler import scraper


class ScraperParsingTests(unittest.TestCase):
    def test_extract_job_links_from_current_markup_normalizes_and_deduplicates(self) -> None:
        html = """
        <html>
          <body>
            <a href="/job-listing/dev-backend-empresa-JV_IC2514646_KO0,11_KE12,19.htm">vaga 1</a>
            <a href="/job-listing/dev-backend-empresa-JV_IC2514646_KO0,11_KE12,19.htm">vaga 1 dup</a>
            <a href="https://www.glassdoor.com.br/job-listing/data-engineer-empresa-JV_IC2514646.htm">vaga 2</a>
            <a href="/Vaga/belo-horizonte.htm">nao e vaga</a>
          </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")

        links = scraper._extract_job_links_from_search_soup(soup)

        self.assertEqual(
            links,
            [
                "https://www.glassdoor.com/job-listing/dev-backend-empresa-JV_IC2514646_KO0,11_KE12,19.htm",
                "https://www.glassdoor.com.br/job-listing/data-engineer-empresa-JV_IC2514646.htm",
            ],
        )

    def test_extract_search_bootstrap_for_pagination_from_next_payload(self) -> None:
        decoded_payload = (
            '{"searchContext":{"absoluteUrl":"https://www.glassdoor.com.br/Vaga/base.htm"},'
            '"queryString":"loc=br","filterParams":[{"key":"seniorityType","value":"entry"}],'
            '"searchUrlParams":{},"isLoggedIn":false,"jobListingIdFromUrl":123456,'
            '"occupationParam":"python","locationId":"2514646","locationType":"C",'
            '"parameterUrlInput":"python-em-belo-horizonte","seoFriendlyUrlInput":"python-bh",'
            '"seoUrl":true,"paginationCursors":[{"cursor":"cursor-page-2","pageNumber":2},'
            '{"cursor":"cursor-page-3","pageNumber":3}]}'
        )
        html = f"<html><script>self.__next_f.push([1,{json.dumps(decoded_payload)}])</script></html>"
        soup = BeautifulSoup(html, "html.parser")

        bootstrap = scraper._extract_search_bootstrap_for_pagination(soup)

        self.assertIsNotNone(bootstrap)
        assert bootstrap is not None
        self.assertEqual(bootstrap["absolute_url"], "https://www.glassdoor.com.br/Vaga/base.htm")
        self.assertEqual(bootstrap["query_string"], "loc=br")
        self.assertEqual(bootstrap["filter_params"], [{"key": "seniorityType", "value": "entry"}])
        self.assertFalse(bootstrap["is_logged_in"])
        self.assertEqual(bootstrap["job_listing_id_from_url"], 123456)
        self.assertEqual(bootstrap["keyword"], "python")
        self.assertEqual(bootstrap["location_id"], 2514646)
        self.assertEqual(bootstrap["location_type"], "CITY")
        self.assertEqual(bootstrap["parameter_url_input"], "python-em-belo-horizonte")
        self.assertEqual(bootstrap["seo_friendly_url_input"], "python-bh")
        self.assertTrue(bootstrap["seo_url"])
        self.assertEqual(bootstrap["pagination_cursors"], {2: "cursor-page-2", 3: "cursor-page-3"})

    @mock.patch("glassdoorcrawler.scraper.time.sleep", return_value=None)
    @mock.patch("glassdoorcrawler.scraper._get_links_from_bff_page")
    @mock.patch("glassdoorcrawler.scraper._get_search_page_links_and_bootstrap")
    def test_get_all_links_uses_bff_and_stops_when_page_has_no_new_links(
        self,
        get_first_page_mock: mock.MagicMock,
        get_bff_links_mock: mock.MagicMock,
        _sleep_mock: mock.MagicMock,
    ) -> None:
        link_1 = "https://www.glassdoor.com/job-listing/1.htm"
        link_2 = "https://www.glassdoor.com/job-listing/2.htm"
        link_3 = "https://www.glassdoor.com/job-listing/3.htm"

        get_first_page_mock.return_value = (
            [link_1, link_2],
            {"pagination_cursors": {2: "cursor-page-2", 3: "cursor-page-3"}},
        )
        get_bff_links_mock.side_effect = [
            [link_2, link_3],  # page 2 has 1 new link
            [link_1, link_2],  # page 3 has 0 new links, pagination should stop
        ]

        all_links = scraper.get_all_links(
            num_pages=3,
            base_url="https://www.glassdoor.com.br/Vaga/base.htm",
            delay_seconds=0,
            session=object(),
        )

        self.assertEqual(all_links, [[link_1, link_2], [link_2, link_3]])
        self.assertEqual(
            [call.kwargs["page_number"] for call in get_bff_links_mock.call_args_list],
            [2, 3],
        )

    @mock.patch("glassdoorcrawler.scraper.time.sleep", return_value=None)
    @mock.patch("glassdoorcrawler.scraper.get_position_links")
    @mock.patch("glassdoorcrawler.scraper._get_search_page_links_and_bootstrap")
    def test_get_all_links_fallback_selects_candidate_with_more_new_links(
        self,
        get_first_page_mock: mock.MagicMock,
        get_position_links_mock: mock.MagicMock,
        _sleep_mock: mock.MagicMock,
    ) -> None:
        link_1 = "https://www.glassdoor.com/job-listing/1.htm"
        link_2 = "https://www.glassdoor.com/job-listing/2.htm"
        link_3 = "https://www.glassdoor.com/job-listing/3.htm"

        base_url = "https://www.glassdoor.com.br/Vaga/base.htm"

        get_first_page_mock.return_value = ([link_1], None)

        def links_for_candidate(url: str, session: object) -> list[str]:
            mapping = {
                f"{base_url}?page=2": [link_1],
                f"{base_url}?p=2": [link_1, link_2],
                "https://www.glassdoor.com.br/Vaga/base_IP2.htm": [link_2, link_3],
                "https://www.glassdoor.com.br/Vaga/base_P2.htm": [link_1],
            }
            return mapping[url]

        get_position_links_mock.side_effect = links_for_candidate

        all_links = scraper.get_all_links(
            num_pages=2,
            base_url=base_url,
            delay_seconds=0,
            session=object(),
        )

        self.assertEqual(all_links, [[link_1], [link_2, link_3]])
        self.assertEqual(
            [call.args[0] for call in get_position_links_mock.call_args_list],
            [
                f"{base_url}?page=2",
                f"{base_url}?p=2",
                "https://www.glassdoor.com.br/Vaga/base_IP2.htm",
            ],
        )

    @mock.patch("glassdoorcrawler.scraper._get")
    def test_scrap_job_page_uses_jsonld_fallback_when_initial_state_is_missing(
        self,
        get_mock: mock.MagicMock,
    ) -> None:
        payload = {
            "@context": "https://schema.org",
            "@type": "JobPosting",
            "title": "Software Engineer",
            "hiringOrganization": {"name": "ACME"},
            "jobLocation": [
                {
                    "address": {
                        "addressLocality": "Belo Horizonte",
                        "addressRegion": "MG",
                    }
                }
            ],
            "salaryCurrency": "BRL",
            "baseSalary": {"value": {"minValue": 5000, "maxValue": 9000, "value": 7000}},
            "description": "Trabalhar com Python e APIs.",
        }
        html = (
            "<html><body>"
            f"<script type='application/ld+json'>{json.dumps(payload)}</script>"
            "</body></html>"
        )
        get_mock.return_value = SimpleNamespace(text=html)

        result = scraper.scrap_job_page("https://www.glassdoor.com/job-listing/1.htm", session=object())

        self.assertEqual(result["job_title"], "Software Engineer")
        self.assertEqual(result["company_name"], "ACME")
        self.assertEqual(result["location"], "Belo Horizonte, MG")
        self.assertEqual(result["salary_estimated"], "BRL 7000")
        self.assertEqual(result["salary_min"], 5000)
        self.assertEqual(result["salary_max"], 9000)
        self.assertEqual(result["job_description"], "Trabalhar com Python e APIs.")

    def test_get_links_from_bff_page_uses_json_for_standard_session_contract(self) -> None:
        class _StandardSession:
            def __init__(self, response: mock.Mock) -> None:
                self.response = response
                self.called_with: dict[str, object] = {}

            def post(
                self,
                url: str,
                headers: dict[str, str],
                timeout: int,
                json: dict[str, object],
            ) -> mock.Mock:
                self.called_with = {
                    "url": url,
                    "headers": headers,
                    "timeout": timeout,
                    "json": json,
                }
                return self.response

        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "data": {
                "jobListings": {
                    "jobListings": [
                        {"jobview": {"header": {"seoJobLink": "/job-listing/backend-dev.htm"}}},
                    ]
                }
            }
        }

        session = _StandardSession(response)
        links = scraper._get_links_from_bff_page(
            page_number=2,
            bootstrap={"pagination_cursors": {2: "cursor-page-2"}},
            session=session,
        )

        self.assertEqual(
            links,
            ["https://www.glassdoor.com/job-listing/backend-dev.htm"],
        )
        self.assertEqual(
            session.called_with["url"],
            scraper.JOB_SEARCH_RESULTS_BFF_URL,
        )
        self.assertIn("json", session.called_with)

    def test_get_links_from_bff_page_falls_back_to_json_payload_for_legacy_session(self) -> None:
        class _LegacySession:
            def __init__(self, response: mock.Mock) -> None:
                self.response = response
                self.used_json_payload = False

            def post(
                self,
                url: str,
                headers: dict[str, str],
                timeout: int,
                json_payload: dict[str, object],
            ) -> mock.Mock:
                self.used_json_payload = True
                return self.response

        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"data": {"jobListings": {"jobListings": []}}}

        session = _LegacySession(response)
        links = scraper._get_links_from_bff_page(
            page_number=2,
            bootstrap={"pagination_cursors": {2: "cursor-page-2"}},
            session=session,
        )

        self.assertEqual(links, [])
        self.assertTrue(session.used_json_payload)


class ScraperOutputPolicyTests(unittest.TestCase):
    def test_cli_default_output_path_matches_policy(self) -> None:
        args = cli.build_parser().parse_args([])
        self.assertEqual(args.output, scraper.DEFAULT_OUTPUT_PATH)

    def test_crawl_jobs_default_output_path_matches_policy(self) -> None:
        output_default = inspect.signature(scraper.crawl_jobs).parameters["output_path"].default
        self.assertEqual(output_default, scraper.DEFAULT_OUTPUT_PATH)

    @mock.patch("glassdoorcrawler.scraper.pd.DataFrame.to_excel", return_value=None)
    @mock.patch("glassdoorcrawler.scraper.pd.ExcelWriter")
    @mock.patch("glassdoorcrawler.scraper.Path.mkdir", autospec=True)
    @mock.patch("glassdoorcrawler.scraper.get_all_links", return_value=[])
    @mock.patch("glassdoorcrawler.scraper._build_session")
    def test_crawl_jobs_creates_missing_output_directory(
        self,
        build_session_mock: mock.MagicMock,
        _get_all_links_mock: mock.MagicMock,
        mkdir_mock: mock.MagicMock,
        excel_writer_mock: mock.MagicMock,
        _to_excel_mock: mock.MagicMock,
    ) -> None:
        session_mock = mock.Mock()
        build_session_mock.return_value = session_mock
        excel_writer_mock.return_value.__enter__.return_value = mock.Mock()

        df = scraper.crawl_jobs(
            base_url="https://example.com/jobs",
            output_path="dataset/local/result.xlsx",
        )

        self.assertTrue(df.empty)
        mkdir_mock.assert_called_once()
        self.assertEqual(mkdir_mock.call_args.kwargs, {"parents": True, "exist_ok": True})
        session_mock.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
