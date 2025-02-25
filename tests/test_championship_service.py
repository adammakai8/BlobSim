import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from domain.championship_service import end_eon_if_over, end_season_if_over
from domain.dtos.league_dto import LeagueDto
from domain.dtos.grandmaster_standings_dto import GrandmasterStandingsDTO
from domain.dtos.standings_dto import StandingsDTO
from data.model.blob import Blob
from domain.utils.constants import GRANDMASTER_PRIZE, CHAMPION_PRIZE, CYCLES_PER_EON


class TestChampionshipService(unittest.TestCase):

    @patch('domain.championship_service.count_unconcluded_for_league')
    @patch('domain.championship_service.get_grandmaster_standings')
    @patch('domain.championship_service.get_blob_by_id')
    @patch('domain.championship_service.save_blob')
    def test_end_eon_if_over(self, mock_save_blob, mock_get_blob_by_id, mock_get_grandmaster_standings, mock_count_unconcluded):
        session = MagicMock(spec=Session)
        league = LeagueDto(id=1, name='League 1', field_size=5, level=1)
        season = 4

        mock_count_unconcluded.return_value = 0
        mock_get_grandmaster_standings.return_value = [
            GrandmasterStandingsDTO(blob_id=1, name="Test Blob", championships=3, gold=5, silver=4, bronze=3, points=100),
            GrandmasterStandingsDTO(blob_id=2, name="Blob Doe", championships=1, gold=5, silver=4, bronze=3, points=100),
            ]
        mock_blob = Blob(id=1, name="Test Blob", grandmasters=0, money=0, contract=0, integrity=0)
        mock_get_blob_by_id.return_value = mock_blob

        result = end_eon_if_over(season, league, session)

        self.assertIsNotNone(result)
        self.assertEqual(mock_blob.grandmasters, 1)
        self.assertEqual(mock_blob.money, GRANDMASTER_PRIZE)
        self.assertEqual(mock_blob.contract, 1)
        self.assertEqual(mock_blob.integrity, CYCLES_PER_EON)
        mock_save_blob.assert_called_once_with(session, mock_blob)

    @patch('domain.championship_service.count_unconcluded_for_league')
    @patch('domain.championship_service.get_standings')
    @patch('domain.championship_service.get_all_by_league_order_by_id')
    @patch('domain.championship_service.save_all_blobs')
    def test_end_season_if_over(self, mock_save_all_blobs, mock_get_all_by_league_order_by_id, mock_get_standings, mock_count_unconcluded):
        session = MagicMock(spec=Session)
        mock_standings = [
            StandingsDTO(blob_id=1, name="Blob 1", is_contract_ending=False, results=[], total_points=100),
            StandingsDTO(blob_id=2, name="Blob 2", is_contract_ending=False, results=[], total_points=90),
            StandingsDTO(blob_id=3, name="Blob 3", is_contract_ending=False, results=[], total_points=80),
            StandingsDTO(blob_id=4, name="Blob 4", is_contract_ending=False, results=[], total_points=70),
            StandingsDTO(blob_id=5, name="Blob 5", is_contract_ending=False, results=[], total_points=60)
        ]
        mock_get_standings.return_value = mock_standings

        def run_test_for_level(level):
            mock_blobs = {
                1: Blob(id=1, name="Blob 1", contract=0, championships=0, season_victories=0, money=0),
                2: Blob(id=2, name="Blob 2", contract=0, championships=0, season_victories=0, money=0),
                3: Blob(id=3, name="Blob 3", contract=0, championships=0, season_victories=0, money=0),
                4: Blob(id=4, name="Blob 4", contract=0, championships=0, season_victories=0, money=0),
                5: Blob(id=5, name="Blob 5", contract=0, championships=0, season_victories=0, money=0)
            }
            mock_get_all_by_league_order_by_id.return_value = mock_blobs

            league = LeagueDto(id=level, name=f'League {level}', field_size=2, level=level)
            season = 1

            mock_count_unconcluded.return_value = 0

            result = end_season_if_over(league, season, session)

            self.assertIsNotNone(result)
            self.assertEqual(mock_blobs[1].contract, 2)
            self.assertEqual(mock_blobs[1].championships, 1 if level == 1 else 0)
            self.assertEqual(mock_blobs[1].season_victories, 1 if level > 1 else 0)
            self.assertEqual(mock_blobs[1].money, CHAMPION_PRIZE)
            self.assertEqual(mock_blobs[2].contract, 1)
            self.assertEqual(mock_blobs[2].championships, 0)
            self.assertEqual(mock_blobs[2].season_victories, 0)
            self.assertEqual(mock_blobs[2].money, 0)
            self.assertEqual(mock_blobs[4].contract, 0)
            self.assertEqual(mock_blobs[4].championships, 0)
            self.assertEqual(mock_blobs[4].season_victories, 0)
            self.assertEqual(mock_blobs[4].money, 0)
            mock_save_all_blobs.assert_called_with(session, list(mock_blobs.values()))

        run_test_for_level(1)
        run_test_for_level(2)


if __name__ == '__main__':
    unittest.main()
