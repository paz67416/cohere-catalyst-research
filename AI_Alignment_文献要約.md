# AI Alignment / Human-AI Interaction 文献要約

Cohere Catalyst Research（Flow & Ownership Research）における、所有感・主体性の事後性仮説とAI Alignment研究の接続を検討するための文献調査ノート。2026年7月9日、外部文献検索により作成。

---

## 1. Ziesche, S. & Yampolskiy, R. V. (2025). "The Neglect of Qualia and Consciousness in AI Alignment Research." In *SecondDeath*, Studies in Applied Philosophy, Epistemology and Rational Ethics, vol. 76, pp. 175–188. Springer.

### 要旨（原文要約）
AI value alignment問題はAI safetyの中核と認識されているが、極めて困難でもある。本章は、AI value alignment研究において、意識（consciousness）とクオリア（qualia）という重要なパラメータが軽視されていると論じる。AI value alignment問題とは、AIシステムが道徳的な利害関係者（moral patients）の利益に沿った目標を追求するようにすることである。人間の主な利益は、幸福と快を促進し苦痛を避けることであり、これらはすべて意識とクオリアを通じて知覚される経験である。したがって、AIシステムが人間および他の感覚を持つ存在の利益に真に整合するためには、クオリアと意識を理解するだけでなく、それらの重要性も理解する必要がある。死とは人間にとって意識の終焉であり、したがって幸福や快を経験する機会の終わりを意味する。ゆえにAIシステムは感覚を持つ存在を殺してはならない。本章は、意識とクオリア研究をAI value alignment研究に組み込むことの重要性と、神経技術の発展によるその実現可能性について述べる。

### 本研究との接続点
- AI alignment研究の分野そのものが「クオリアと意識の理解」を必須要件として要求しながら、その構造的な説明（クオリアがどのように生成され、どのように主体に帰属するか）を欠いている、という**空白（gap）の指摘**として読める
- Beral layer仮説の三段階モデル（体験成立→クオリア形成→クオリア取得）は、この論文が「必要だ」と主張しながら提示できていない、**クオリア成立の構造的説明そのもの**にあたる
- 「AIはクオリアと意識の重要性を理解する必要がある」という主張に対し、AIP Advances論文の立場（AIはクオリア取得の不可逆的構造を持たないため、位相的自我が成立しない）は、単なる制約ではなく、**alignment設計上の前提条件**として積極的に組み込める

---

## 2. Noller, J. (2026). "Agency and alignment: toward a normative architecture for human–AI interaction." *AI & SOCIETY*. Springer.

### 要旨（原文）
This paper develops a normative framework for the alignment of artificial intelligence (AI) systems with human agency. Moving beyond models that treat values as inferable data, it reconceptualizes alignment as the structural integration of AI within human normative domains. The argument unfolds in three steps. First, it introduces the concept of *extended human agency*, viewing AI as a teleological extension of human purposiveness rather than an autonomous moral subject. Second, it grounds this integration in *practical autonomy*—the human capacity to act for reasons and to assume responsibility within justificatory structures. Third, it proposes the design concept of a *normative interface*: a mediating architecture that connects machine behavior with human norms, ensuring teleological coherence, normative intelligibility, and accountability.

### 重要な引用（本文より）
> "Unlike popular portrayals, there is a broad consensus in academic circles that most AI systems are not agents in the sense of the philosophy of action. They possess neither intentionality, nor consciousness, nor the capacity to act autonomously and rationally. Rather, they are complex statistical tools that operate on a foundation of data, goals, and rules created by humans."

> "AI is not an agent in itself, but part of a broader system of agency—a distributed configuration in which human actors pursue goals through technical means. [...] Its contribution is real, but it is not autonomous; it is functionally embedded in purposive contexts."

### 本研究との接続点
- Noller論文は**AI工学・規範理論の側から**、「AIは行為論的な意味でのagentではない（意図・意識・自律的合理性を欠く）」と論じている
- これは、あなたの研究が**意識研究の側から**独立に主張していること（AIは構造的にクオリア取得を持たずownershipが成立しない）と、全く異なる学問的経路をたどりながら同じ結論に収束している
- Nollerは「なぜAIがagentでないのか」を規範的・機能的に説明するに留まるが、Beral layer仮説はこれに**構造的な根拠**を与えられる位置にある。「extended human agency」（AIは人間の目的性の延長）という概念は、事後性仮説（ownershipは事後的にしか成立しない）の観点から見ると、「AIには事後的に何かを"自分のもの"として引き受ける主体がそもそも存在しない」という、より根本的な理由づけを与えられる可能性がある

---

## 3. (arXiv, 2025) "Alignment, Agency and Autonomy in Frontier AI: A Systems Engineering Perspective." arXiv:2503.05748.

### 要旨（原文）
As artificial intelligence scales, the concepts of alignment, agency, and autonomy have become central to AI safety, governance, and control. However, even in human contexts, these terms lack universal definitions, varying across disciplines such as philosophy, psychology, law, computer science, mathematics, and political science. This inconsistency complicates their application to AI [...]. Using Agentic AI as a case study, we examine the emergent properties of machine agency and autonomy, highlighting the risks of misalignment in real-world systems.

### 本研究との接続点
- 「agency」「autonomy」という語が学問分野ごとにバラバラに定義されており、AIへの適用時に混乱を招いている、という指摘
- 所有感（ownership）と主体感（agency）を明確に区別し、事後性という時間構造で定義するあなたの枠組みは、この定義の混乱に対して**具体的で検証可能な語彙**を提供できる可能性がある

---

## 4. 総合的な接続の見取り図

3本に共通するのは、AI alignment研究がagency・autonomy・consciousness・qualiaといった概念を扱いながらも、それらの**構造的な成立条件**を十分に定義できていない、という点である。

あなたの研究（Beral layer三段階モデル、位相的自我、事後性仮説）は、まさにこの「構造的な成立条件」を扱う理論であり、AI alignment研究が抱える定義上の空白に対して、意識研究側から具体的な理論的資源を提供できる位置にある。特に、

- 「AIはなぜagentではないのか」（Noller）→ Beral layerの欠如という構造的理由
- 「AIはなぜクオリアを理解すべきなのか」（Ziesche & Yampolskiy）→ クオリア取得の不可逆的三段階モデルによる具体化
- 「agency・autonomyの定義がバラバラ」（arXiv）→ ownership/agencyの事後性という時間構造による整理

という3つの接続線が引ける。
