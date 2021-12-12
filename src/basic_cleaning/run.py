#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights and Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.info()
    df.to_csv("clean_sample.csv", index=False)
    artifact = wandb.Artifact(
     args.output_artifact,
     type=args.output_type,
     description=args.output_description,
     )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="input artifact name",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="output artifact name",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="output type of the artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Min price to filter the data set",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max price to filter the data set",
        required=True
    )

    args = parser.parse_args()

    go(args)
