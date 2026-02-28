import argparse
from pathlib import Path

DATASET_ORDER = ["Blur", "Haze", "Lowlight", "Rain", "Snow"]
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


def build_prefix(dataset: str, index: int) -> str:
    if dataset[:1].isdigit():
        return dataset
    return f"{dataset}"


def collect_pairs(root_dir: Path, dataset: str, prefix: str) -> tuple[list[str], int]:
    gt_dir = root_dir / dataset / "GT"
    lq_dir = root_dir / dataset / "LQ"
    if not gt_dir.is_dir() or not lq_dir.is_dir():
        print(f"Skip {dataset}: missing GT/LQ")
        return [], 0

    names = sorted(
        p.name for p in gt_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTS
    )

    lines = []
    missing = 0
    for name in names:
        if not (lq_dir / name).is_file():
            missing += 1
            continue
        lines.append(f"{prefix}/GT/{name}, {prefix}/LQ/{name}")
    return lines, missing


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-dir", default="./train_data", type=str)
    parser.add_argument("--output", default="Trainset_meta_info1.txt", type=str)
    args = parser.parse_args()

    root_dir = Path(args.root_dir)
    out_path = Path(args.output)

    all_lines = []
    total_missing = 0

    for idx, dataset in enumerate(DATASET_ORDER, start=1):
        prefix = build_prefix(dataset, idx)
        lines, missing = collect_pairs(root_dir, dataset, prefix)
        all_lines.extend(lines)
        total_missing += missing

    out_path.write_text("\n".join(all_lines) + ("\n" if all_lines else ""), encoding="utf-8")
    print(f"Wrote {len(all_lines)} lines to {out_path}")
    if total_missing:
        print(f"Skipped {total_missing} GT entries with missing LQ")


if __name__ == "__main__":
    main()