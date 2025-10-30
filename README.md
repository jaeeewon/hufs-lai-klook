# hufs-lai-klook

Division of Language & AI, HUFS

## Project Overview

본 프로젝트는 한국외국어대학교 Language & AI융합학부와 Klook(클룩)의 산학협력 프로젝트의 일환으로, 저희 7조는 모든 열차 상품을 배정받았습니다. \
저는 영어-한국어 번역 품질을 자동으로 평가하기 위해 'LLM-as-a-judge' 시스템을 구축했습니다. \
최종적으로, 부족함이 있는 번역을 더 잘 커버하도록 Klook에서 사용되는 프롬프트를 개선하게 됩니다.

## Members
<table>
    <tr>
        <td align="center" width="150px">
            <a href="https://github.com/jaeeewon"><img height="80px"  src="https://avatars.githubusercontent.com/u/87597383"></a>
            <br/>
            <small>Language & AI</small>
            </br>
            <small>202402050</small>
            <br />
            <a href="https://github.com/jaeeewon"><strong>최재원</strong></a>
            <br />
        </td>
    </tr>
</table>

## Current Status

'LLM-as-a-judge'에서 **평가 프롬프트**를 엔지니어링하고 있습니다.

### Model Selection

- **초기 테스트:** `Qwen/Qwen3-32B` 모델을 기반으로 'LLM-as-a-judge'의 가능성을 검증했습니다.
- **성능 개선:** 복잡한 규칙 준수 및 추론 능력 한계를 극복하기 위해, 더 강력한 모델을 검토 중입니다.

## Tech Stack

- **Inference:** `vLLM`, A high-throughput and memory-efficient inference and serving engine for LLMs
- **GPU:** 4 x NVIDIA RTX 5090 (32GB)
- **Model:** `Qwen3-30B-A3B-Instruct-2507`

## Plans

- [x] **LLM-as-a-judge:** 더 큰 모델을 사용하여 instruction-following rate 및 정확도 확보
- [ ] **Manual:** 'LLM-as-a-judge'로 생성된 고품질 평가 데이터를 기반으로 Klook에서 사용되는 프롬프트를 개선
    - 아직 좋은 아이디어가 떠오르지 않음
- [ ] **Crawl Items:** Klook의 관광 상품에 대해서도 크롤링 및 평가하여 프롬프트 개선
