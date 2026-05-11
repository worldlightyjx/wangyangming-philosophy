from __future__ import annotations

import json
import re
from pathlib import Path

import pdfplumber


ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "王阳明全集（隆庆初刻本增补全本，简体横排） (【明朝】王阳明) (z-library.sk, 1lib.sk, z-lib.sk).pdf"
DATA_DIR = ROOT / "data"
VOLUME_DIR = DATA_DIR / "volumes"
BAIHUA_DIR = DATA_DIR / "baihua"


VOLUMES = [
    {"id": "juan01-cxl-shang", "book": 1, "juan": 1, "primary": "语录一", "secondary": "传习录上", "start_page": 70},
    {"id": "juan02-cxl-zhong", "book": 1, "juan": 2, "primary": "语录二", "secondary": "传习录中", "start_page": 174},
    {"id": "juan03-cxl-xia", "book": 1, "juan": 3, "primary": "语录三", "secondary": "传习录下", "start_page": 298},
    {"id": "juan04-wenlu-shuyi", "book": 1, "juan": 4, "primary": "文录一", "secondary": "书一", "start_page": 436},
    {"id": "juan05-wenlu-shuer", "book": 1, "juan": 5, "primary": "文录二", "secondary": "书二", "start_page": 511},
    {"id": "juan06-wenlu-shusan", "book": 1, "juan": 6, "primary": "文录三", "secondary": "书三", "start_page": 563},
    {"id": "juan07-wenlu-xujishuo", "book": 1, "juan": 7, "primary": "文录四", "secondary": "序记说", "start_page": 619},
    {"id": "juan08-wenlu-zazhu", "book": 1, "juan": 8, "primary": "文录五", "secondary": "杂著", "start_page": 715},
    {"id": "juan09-bielu-zoushuyi", "book": 2, "juan": 9, "primary": "别录一", "secondary": "奏疏一", "start_page": 751},
    {"id": "juan10-bielu-zoushuer", "book": 2, "juan": 10, "primary": "别录二", "secondary": "奏疏二", "start_page": 840},
    {"id": "juan11-bielu-zoushusan", "book": 2, "juan": 11, "primary": "别录三", "secondary": "奏疏三", "start_page": 901},
    {"id": "juan12-bielu-zoushusi", "book": 2, "juan": 12, "primary": "别录四", "secondary": "奏疏四", "start_page": 985},
    {"id": "juan13-bielu-zoushuwu", "book": 2, "juan": 13, "primary": "别录五", "secondary": "奏疏五", "start_page": 1064},
    {"id": "juan14-bielu-zoushuliu", "book": 2, "juan": 14, "primary": "别录六", "secondary": "奏疏六", "start_page": 1140},
    {"id": "juan15-bielu-zoushuqi", "book": 2, "juan": 15, "primary": "别录七", "secondary": "奏疏七", "start_page": 1209},
    {"id": "juan16-bielu-gongyiyi", "book": 2, "juan": 16, "primary": "别录八", "secondary": "公移一", "start_page": 1279},
    {"id": "juan17-bielu-gongyier", "book": 2, "juan": 17, "primary": "别录九", "secondary": "公移二", "start_page": 1380},
    {"id": "juan18-bielu-gongyisan", "book": 2, "juan": 18, "primary": "别录十", "secondary": "公移三", "start_page": 1491},
    {"id": "juan19-waiji-fusaoshi", "book": 3, "juan": 19, "primary": "外集一", "secondary": "赋骚诗", "start_page": 1573},
    {"id": "juan20-waiji-shi", "book": 3, "juan": 20, "primary": "外集二", "secondary": "诗", "start_page": 1723},
    {"id": "juan21-waiji-shu", "book": 3, "juan": 21, "primary": "外集三", "secondary": "书", "start_page": 1912},
    {"id": "juan22-waiji-xu", "book": 3, "juan": 22, "primary": "外集四", "secondary": "序", "start_page": 1994},
    {"id": "juan23-waiji-ji", "book": 3, "juan": 23, "primary": "外集五", "secondary": "记", "start_page": 2036},
    {"id": "juan24-waiji-shuozazhu", "book": 3, "juan": 24, "primary": "外集六", "secondary": "说 杂著", "start_page": 2080},
    {"id": "juan25-waiji-muzhiming", "book": 3, "juan": 25, "primary": "外集七", "secondary": "墓志铭 墓表 墓碑 传 碑刻 赞 箴 祭文", "start_page": 2128},
    {"id": "juan26-xubian-yi", "book": 3, "juan": 26, "primary": "续编一", "secondary": "", "start_page": 2218},
    {"id": "juan27-xubian-shu", "book": 3, "juan": 27, "primary": "续编二", "secondary": "书", "start_page": 2280},
    {"id": "juan28-xubian-zazhu", "book": 3, "juan": 28, "primary": "续编三", "secondary": "杂著", "start_page": 2326},
    {"id": "juan29-xubian-si", "book": 3, "juan": 29, "primary": "续编四", "secondary": "", "start_page": 2377},
    {"id": "juan30-xubian-sanzheng", "book": 3, "juan": 30, "primary": "续编五", "secondary": "三征公移逸稿", "start_page": 2462},
    {"id": "juan31-xubian-liu", "book": 3, "juan": 31, "primary": "续编六", "secondary": "", "start_page": 2579},
    {"id": "juan32-nianpuyi", "book": 4, "juan": 32, "primary": "年谱一", "secondary": "", "start_page": 2738},
    {"id": "juan33-nianpuer", "book": 4, "juan": 33, "primary": "年谱二", "secondary": "", "start_page": 2831},
    {"id": "juan34-nianpusan", "book": 4, "juan": 34, "primary": "年谱三", "secondary": "", "start_page": 2892},
    {"id": "juan35-nianpu-fuluyi", "book": 4, "juan": 35, "primary": "年谱附录一", "secondary": "", "start_page": 2995},
    {"id": "juan36-nianpu-fuluer", "book": 4, "juan": 36, "primary": "年谱附录二", "secondary": "", "start_page": 3065},
    {"id": "juan37-shideji", "book": 4, "juan": 37, "primary": "世德纪", "secondary": "", "start_page": 3117},
    {"id": "juan38-shideji-fulu", "book": 4, "juan": 38, "primary": "世德纪附录", "secondary": "", "start_page": 3291},
    {"id": "juan39-weikan-yulu-shiwen", "book": 4, "juan": 39, "primary": "旧本未刊语录诗文补编", "secondary": "", "start_page": 3425},
    {"id": "juan40-weikan-jiwen-zhuanji", "book": 4, "juan": 40, "primary": "旧本未刊祭文传记补编", "secondary": "", "start_page": 3538},
]


def normalize_text(text: str) -> str:
    text = text.replace("\u3000", "")
    text = re.sub(r"\s+", "", text)
    return text.strip()


def extract_lines(page) -> list[dict]:
    words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
    rows = {}
    for word in words:
        rows.setdefault(round(word["top"], 1), []).append(word)

    lines = []
    for top in sorted(rows):
        row_words = sorted(rows[top], key=lambda item: item["x0"])
        text = normalize_text("".join(word["text"] for word in row_words))
        if not text:
            continue
        lines.append({"top": top, "x0": round(row_words[0]["x0"], 1), "text": text})
    return lines


def classify_block(text: str) -> str:
    compact = normalize_text(text)
    if len(compact) <= 18 and re.search(r"(年|月|日|甲|乙|丙|丁|戊|己|庚|辛|壬|癸|正德|嘉靖|弘治|成化|隆庆)", compact):
        return "meta"
    if len(compact) <= 30 and not re.search(r"[。！？；：”』》）)]$", compact):
        return "heading"
    return "para"


def build_blocks(doc, volume: dict) -> list[dict]:
    blocks: list[dict] = []
    current: dict | None = None
    header_texts = {normalize_text(volume["primary"])}
    if volume["secondary"]:
        header_texts.add(normalize_text(volume["secondary"]))

    for page_no in range(volume["start_page"], volume["end_page"] + 1):
        lines = extract_lines(doc.pages[page_no - 1])

        if page_no == volume["start_page"]:
            lines = [line for line in lines if normalize_text(line["text"]) not in header_texts]

        for line in lines:
            text = line["text"]
            if not text:
                continue

            if current is None or line["x0"] >= 25:
                current = {
                    "type": classify_block(text),
                    "wen": text,
                    "bai": "",
                    "page": page_no,
                }
                blocks.append(current)
            else:
                current["wen"] += text
                if current["type"] in {"heading", "meta"}:
                    compact = normalize_text(current["wen"])
                    if len(compact) > 40:
                        current["type"] = "para"

    return blocks


def dump_js(path: Path, var_name: str, payload) -> None:
    path.write_text(
        f"window.{var_name} = {json.dumps(payload, ensure_ascii=False)};\n",
        encoding="utf-8",
    )


def dump_volume_js(path: Path, volume_id: str, payload) -> None:
    path.write_text(
        "window.BOOK_VOLUMES = window.BOOK_VOLUMES || {};\n"
        f"window.BOOK_VOLUMES[{json.dumps(volume_id, ensure_ascii=False)}] = "
        f"{json.dumps(payload, ensure_ascii=False)};\n",
        encoding="utf-8",
    )


def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(PDF_PATH)

    DATA_DIR.mkdir(exist_ok=True)
    VOLUME_DIR.mkdir(exist_ok=True)

    for idx, volume in enumerate(VOLUMES):
        volume["end_page"] = VOLUMES[idx + 1]["start_page"] - 1 if idx + 1 < len(VOLUMES) else 3750

    index = {
        "title": "王阳明全集",
        "total_pages": 3750,
        "baihua_ids": sorted(path.stem for path in BAIHUA_DIR.glob("*.js")) if BAIHUA_DIR.exists() else [],
        "volumes": [],
    }

    with pdfplumber.open(str(PDF_PATH)) as doc:
        for volume in VOLUMES:
            blocks = build_blocks(doc, volume)
            payload = {
                "id": volume["id"],
                "book": volume["book"],
                "juan": volume["juan"],
                "primary": volume["primary"],
                "secondary": volume["secondary"],
                "title": f"卷{volume['juan']} {volume['primary']}" + (f" · {volume['secondary']}" if volume["secondary"] else ""),
                "start_page": volume["start_page"],
                "end_page": volume["end_page"],
                "block_count": len(blocks),
                "blocks": blocks,
            }
            dump_volume_js(VOLUME_DIR / f"{volume['id']}.js", volume["id"], payload)
            index["volumes"].append(
                {
                    "id": payload["id"],
                    "book": payload["book"],
                    "juan": payload["juan"],
                    "primary": payload["primary"],
                    "secondary": payload["secondary"],
                    "title": payload["title"],
                    "start_page": payload["start_page"],
                    "end_page": payload["end_page"],
                    "block_count": payload["block_count"],
                }
            )

    dump_js(DATA_DIR / "book-index.js", "BOOK_INDEX", index)
    print(f"generated {len(index['volumes'])} volumes into {VOLUME_DIR}")


if __name__ == "__main__":
    main()
