import pandas as pd


class DataFrameDataset:
    def __init__(self, df, columns):
        self.df = df
        self.columns = columns
        # ['question_id', 'model_a', 'model_b', 'winner', 'judge', 'conversation_a', 'conversation_b', 'turn']

    def __iter__(self):
        for index, row in self.df.iterrows():
            yield [row[col] for col in self.columns]


def fetch_dataset(name: str) -> DataFrameDataset:
    splits = {
        'gpt4_pair': 'data/gpt4_pair-00000-of-00001-c0b431264a82ddc0.parquet',
        'human': 'data/human-00000-of-00001-25f4910818759289.parquet'
    }
    df = pd.read_parquet("hf://datasets/lmsys/mt_bench_human_judgments/" + splits[name])

    return DataFrameDataset(df, df.columns)


def download_dataset(data_dir: str) -> None:
    from datasets import load_dataset

    dataset = load_dataset("lmsys/mt_bench_human_judgments")
    dataset["human"].to_json(f"{data_dir}/human_judgments.json")
    dataset["gpt4_pair"].to_json(f"{data_dir}/gpt4_pair_judgments.json")
