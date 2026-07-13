# -*- coding: utf-8 -*-
"""
analyze_switch.py

「スイッチ仮説」の批判的分析を Cohere Command A に依頼するスクリプト。

前提:
  - $env:CO_API_KEY に Production キーが設定されていること
  - 同じフォルダに cohere-instruction-v1.md があること(ask.py と同じ system prompt)
  - cohere ライブラリがインストール済み( pip install cohere )

使い方(PowerShell):
  .\venv\Scripts\Activate.ps1
  python analyze_switch.py

出力:
  - 標準出力に分析結果を表示
  - switch_analysis_output.md に保存
"""

import os
import sys
import cohere

MODEL = "command-a-03-2025"  # ask.py で使っている Command A に合わせる。異なる場合はここを変更。
INSTRUCTION_FILE = "cohere-instruction-v1.md"
OUTPUT_FILE = "switch_analysis_output.md"

# --- スイッチ仮説の記述(今回のブログ記事 cohere-log-013 の骨子) ---
HYPOTHESIS = """
【背景となる立場(既存)】
経験の生成は「事後的」である。クオリアの形成とその獲得(帰属)の間には順序があり、
「私(主体)」はその結果として事後的に立ち上がる(三段階モデル: 経験の成立 → クオリア形成 → クオリア獲得)。
行為所有感(Sense of Ownership)と主体感(Sense of Agency)は区別され、
ゾーン(フロー)状態では Agency が後退する一方で Ownership は維持されるという非対称性が観察される。

【今回の新しい着想: スイッチ仮説】
事後性そのものは常に成立している(一階の構造)。
しかし、その事後性が「どれだけ前景化するか」は一定ではない(二階の構造)。
主体性の前景化には、
  (a)「私」側が前面に出ている状態 と
  (b) より大きな流れ(仮にワンネス的なものと呼ぶ)が前面に出ている状態
があり、この二つが「スイッチ」のように切り替わっているのではないか。
普段は(a)、ゾーン状態では相対的に(a)が後退し(b)寄りになる。
この後退の度合いが「スイッチの位置」として捉えられるのではないか。

構え(kamae, 行為選択に先立つ準備状態)が、このスイッチの傾きを決める条件の一つである可能性がある。
あるいは構えとは別の変数がスイッチを動かしている可能性もある(未確定)。
"""

ANALYSIS_PROMPT = f"""
以下は、意識研究における「スイッチ仮説」という理論的着想です。あなたは厳格だが建設的な査読者として、
この仮説を批判的に分析してください。目的は仮説を潰すことではなく、反証可能で検証可能な形に鍛えることです。

{HYPOTHESIS}

次の観点それぞれについて、日本語で、具体的かつ簡潔に指摘してください。

1. 概念的な弱点・曖昧さ
   - 「スイッチ」「前景化」「ワンネス的なもの」といった概念のうち、操作的定義が欠けているものはどれか。
   - 「一階/二階の構造」という区別は、既存の事後性モデルに対して本当に新しい説明力を持つか。それとも言い換えに過ぎない危険はないか。

2. 反証可能性(Popper 的観点)
   - この仮説が偽であるとしたら、どのような観察が得られるはずか。
   - 現状の記述のままでは、どんな結果が出ても後付けで説明できてしまう(反証不可能な)リスクはあるか。

3. 対抗仮説との識別
   - 「スイッチ(離散的な切り替え)」ではなく「連続的なグラデーション(主体感の強度が連続的に変動するだけ)」で説明した場合と、経験的にどう区別できるか。
   - 単なる注意配分・自己意識の低下(既存のフロー研究)で説明し尽くせてしまう部分はないか。

4. 測定・操作化の提案
   - スイッチの「位置」を測るために、どのような指標(主観報告スケール、反応時間、生理指標、行動指標など)が考えられるか。
   - 構え(kamae)がスイッチの傾きを決めるという主張を検証するための、最小の実験デザインを1つ提案してください。

5. 総合評価
   - この仮説を論文・実験プロトコルに進める上で、最優先で解消すべき弱点を3つ、優先順にまとめてください。

出力は Markdown 形式で、見出しを付けて整理してください。
"""


def load_instruction(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    print(f"[警告] {path} が見つかりません。system prompt なしで続行します。", file=sys.stderr)
    return None


def main():
    api_key = os.environ.get("CO_API_KEY")
    if not api_key:
        print("[エラー] 環境変数 CO_API_KEY が設定されていません。", file=sys.stderr)
        print("PowerShell で $env:CO_API_KEY を設定してから再実行してください。", file=sys.stderr)
        sys.exit(1)

    co = cohere.ClientV2(api_key=api_key)

    system_prompt = load_instruction(INSTRUCTION_FILE)
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": ANALYSIS_PROMPT})

    print(f"[情報] モデル {MODEL} にスイッチ仮説の批判的分析を依頼しています...\n", file=sys.stderr)

    try:
        resp = co.chat(model=MODEL, messages=messages)
    except Exception as e:
        print(f"[エラー] Cohere API 呼び出しに失敗しました: {e}", file=sys.stderr)
        print("MODEL 名が正しいか(ask.py と揃っているか)を確認してください。", file=sys.stderr)
        sys.exit(1)

    # ClientV2 のレスポンスからテキストを取り出す
    text = ""
    try:
        for block in resp.message.content:
            if getattr(block, "type", None) == "text":
                text += block.text
    except Exception:
        text = str(resp)

    print(text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n[情報] 結果を {OUTPUT_FILE} に保存しました。", file=sys.stderr)


if __name__ == "__main__":
    main()