import pandas as pd
from dataclasses import asdict
from domain.models import OutputStats


class ReportGenerator:
    @staticmethod
    def build_shoe_summary_df(output_stats: list[OutputStats]) -> pd.DataFrame:
        return pd.DataFrame([asdict(stats) for stats in output_stats])

