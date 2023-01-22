import re

def fp_extension(raw_fp: str) -> str:
    return re.sub(r"(\\|\\\\|/)", ".", raw_fp[: -raw_fp.endswith('.py') * 3 or None])
