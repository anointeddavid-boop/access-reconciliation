import pandas as pd
import os
import logging
from datetime import datetime

os.makedirs("logs", exist_ok=True)
log_file = "logs/reconciliation_" + datetime.now().strftime("%Y-%m-%d") + ".log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting reconciliation process")
ccure_df   = pd.read_excel("data/ccure.xlsx")
genetec_df = pd.read_excel("data/genetec.xlsx")
logger.info("C-CURE loaded: " + str(len(ccure_df)) + " records")
logger.info("Genetec loaded: " + str(len(genetec_df)) + " records")

ccure_df.columns   = ccure_df.columns.str.strip().str.lower().str.replace(" ", "_")
genetec_df.columns = genetec_df.columns.str.strip().str.lower().str.replace(" ", "_")

ccure_cards   = set(ccure_df["card_number"].dropna().astype(str))
genetec_cards = set(genetec_df["card_number"].dropna().astype(str))

only_in_ccure   = ccure_cards - genetec_cards
only_in_genetec = genetec_cards - ccure_cards
in_both         = ccure_cards & genetec_cards

ccure_only_df   = ccure_df[ccure_df["card_number"].astype(str).isin(only_in_ccure)]
genetec_only_df = genetec_df[genetec_df["card_number"].astype(str).isin(only_in_genetec)]
both_df         = ccure_df[ccure_df["card_number"].astype(str).isin(in_both)]

os.makedirs("output", exist_ok=True)
timestamp   = datetime.now().strftime("%Y-%m-%d") + "_" + datetime.now().strftime("%H-%M")
output_file = "output/reconciliation_" + timestamp + ".xlsx"

logger.info("Writing output file...")
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    ccure_only_df.to_excel(writer,   sheet_name="Only_in_CCURE",   index=False)
    genetec_only_df.to_excel(writer, sheet_name="Only_in_Genetec", index=False)
    both_df.to_excel(writer,         sheet_name="In_Both",         index=False)

logger.info("RECONCILIATION COMPLETE")
logger.info("Only in C-CURE   : " + str(len(only_in_ccure)))
logger.info("Only in Genetec  : " + str(len(only_in_genetec)))
logger.info("In Both          : " + str(len(in_both)))
logger.info("Output saved to  : " + output_file)

print("=" * 40)
print("   RECONCILIATION COMPLETE")
print("=" * 40)
print("  Only in C-CURE   : " + str(len(only_in_ccure)))
print("  Only in Genetec  : " + str(len(only_in_genetec)))
print("  In Both          : " + str(len(in_both)))
print("  Output saved to  : " + output_file)
print("  Log saved to     : " + log_file)
print("=" * 40)