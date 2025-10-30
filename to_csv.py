import pandas as pd, json

records = [
    {
        "error_type": "STYLE GUIDE ISSUE",
        "impact_type": "Minor",
        "source": "Shin Hakodate Hokuto Station",
        "target": "신하코다테호쿠토",
        "offer": "신하코다테호쿠토역(Shin Hakodate Hokuto Station)",
        "reason": "주요 역명은 원문 병기(영문명)가 필요하며, 'Shin Hakodate Hokuto Station'이 누락됨. '역'이 추가되어야 하며, 원문 병기 없이는 고객의 명확한 이해에 어려움이 있음.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": "JR Hokkaido, operated by the Hokkaido Railway Company, serves Japan's northernmost island. It's known for the Hokkaido Shinkansen, which offers quick and comfy travel fromHakodate to Sapporo. The JR Hokkaido trains are great for visiting Hokkaido's famous snow festivals, hot springs, and national parks.Hokkaido ShinkansenThe Hokkaido Shinkansen, consisting of theHayate ShinkansenandHayabusa Shinkansen, is a super-fast train that travels from Aomori on Honshu to Hakodate in Hokkaido. It goes through the amazing Seikan Tunnel, the longest undersea tunnel in the world. It's also a comfy and quick way to head north, stopping at important places like Hakodate and Shin Hakodate Hokuto Station.",
        "orig_translation": "JR 홋카이도는 일본 최북단에 위치한 홋카이도의 다양한 지역을 연결합니다. 하코다테에서 삿포로까지 빠르고 편안하게 이동할 수 있는 노선입니다. JR 홋카이도 열차로 홋카이도의 유명한 눈 축제를 만끽하고, 온천과 스키 리조트, 국립공원 등을 간편하게 방문해보세요.#### 홋카이도 신칸센홋카이도 신칸센은하야테 신칸센과하야부사 신칸센으로 구성되어 있으며, 일본 본섬의 아오모리에서 하코다테까지 빠르게 이동하는 고속 열차입니다. 세계에서 가장 긴 해저 터널인 세이칸 터널을 통과하며, 츠가루 해협의 아름다운 경치를 감상할 수 있습니다. JR 홋카이도에서 운행하는 홋카이도 신칸센은 하코다테와 신하코다테호쿠토 등 주요 정차지를 거치며 일본 최북단까지 빠르고 편안한 이동 경험을 제공해요. 지금 클룩에서 홋카이도 신칸센 티켓을 예약하고 겨울의 홋카이도를 나만의 속도로 즐겨보세요.",
    },
    {
        "error_type": "AWKWARD STYLE & REPETITIONS",
        "impact_type": "Minor",
        "source": "JR Hokkaido, operated by the Hokkaido Railway Company, serves Japan's northernmost island.",
        "target": "JR 홋카이도는 일본 최북단에 위치한 홋카이도의 다양한 지역을 연결합니다.",
        "offer": "JR 홋카이도는 홋카이도 철도 회사가 운영하는 일본 최북단 섬인 홋카이도의 다양한 지역을 연결합니다.",
        "reason": "번역에서 '지역을 연결합니다'라는 표현이 반복되며, '다양한 지역'이라는 표현이 '다양한'이 과도하게 반복됨. '다양한 지역'보다는 '주요 지역'이나 '각지' 등이 더 자연스러움.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": "JR Hokkaido, operated by the Hokkaido Railway Company, serves Japan's northernmost island. It's known for the Hokkaido Shinkansen, which offers quick and comfy travel fromHakodate to Sapporo. The JR Hokkaido trains are great for visiting Hokkaido's famous snow festivals, hot springs, and national parks.Hokkaido ShinkansenThe Hokkaido Shinkansen, consisting of theHayate ShinkansenandHayabusa Shinkansen, is a super-fast train that travels from Aomori on Honshu to Hakodate in Hokkaido. It goes through the amazing Seikan Tunnel, the longest undersea tunnel in the world. It's also a comfy and quick way to head north, stopping at important places like Hakodate and Shin Hakodate Hokuto Station.",
        "orig_translation": "JR 홋카이도는 일본 최북단에 위치한 홋카이도의 다양한 지역을 연결합니다. 하코다테에서 삿포로까지 빠르고 편안하게 이동할 수 있는 노선입니다. JR 홋카이도 열차로 홋카이도의 유명한 눈 축제를 만끽하고, 온천과 스키 리조트, 국립공원 등을 간편하게 방문해보세요.#### 홋카이도 신칸센홋카이도 신칸센은하야테 신칸센과하야부사 신칸센으로 구성되어 있으며, 일본 본섬의 아오모리에서 하코다테까지 빠르게 이동하는 고속 열차입니다. 세계에서 가장 긴 해저 터널인 세이칸 터널을 통과하며, 츠가루 해협의 아름다운 경치를 감상할 수 있습니다. JR 홋카이도에서 운행하는 홋카이도 신칸센은 하코다테와 신하코다테호쿠토 등 주요 정차지를 거치며 일본 최북단까지 빠르고 편안한 이동 경험을 제공해요. 지금 클룩에서 홋카이도 신칸센 티켓을 예약하고 겨울의 홋카이도를 나만의 속도로 즐겨보세요.",
    },
    {
        "error_type": "OVERTRANSLATION",
        "impact_type": "Minor",
        "source": "It's also a comfy and quick way to head north, stopping at important places like Hakodate and Shin Hakodate Hokuto Station.",
        "target": "JR 홋카이도에서 운행하는 홋카이도 신칸센은 하코다테와 신하코다테호쿠토 등 주요 정차지를 거치며 일본 최북단까지 빠르고 편안한 이동 경험을 제공해요.",
        "offer": "또한 하코다테와 신하코다테호쿠토역 등 주요 정차지를 거치며 북쪽으로 빠르고 편안하게 이동할 수 있는 방법입니다.",
        "reason": "'이동 경험을 제공해요'는 원문에 없으며, 'way to head north'라는 표현을 과도하게 확장한 오버트랜슬레이션. '이동 경험'은 마케팅적 표현이지만, 원문은 객관적 설명이므로 부적절함.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": "JR Hokkaido, operated by the Hokkaido Railway Company, serves Japan's northernmost island. It's known for the Hokkaido Shinkansen, which offers quick and comfy travel fromHakodate to Sapporo. The JR Hokkaido trains are great for visiting Hokkaido's famous snow festivals, hot springs, and national parks.Hokkaido ShinkansenThe Hokkaido Shinkansen, consisting of theHayate ShinkansenandHayabusa Shinkansen, is a super-fast train that travels from Aomori on Honshu to Hakodate in Hokkaido. It goes through the amazing Seikan Tunnel, the longest undersea tunnel in the world. It's also a comfy and quick way to head north, stopping at important places like Hakodate and Shin Hakodate Hokuto Station.",
        "orig_translation": "JR 홋카이도는 일본 최북단에 위치한 홋카이도의 다양한 지역을 연결합니다. 하코다테에서 삿포로까지 빠르고 편안하게 이동할 수 있는 노선입니다. JR 홋카이도 열차로 홋카이도의 유명한 눈 축제를 만끽하고, 온천과 스키 리조트, 국립공원 등을 간편하게 방문해보세요.#### 홋카이도 신칸센홋카이도 신칸센은하야테 신칸센과하야부사 신칸센으로 구성되어 있으며, 일본 본섬의 아오모리에서 하코다테까지 빠르게 이동하는 고속 열차입니다. 세계에서 가장 긴 해저 터널인 세이칸 터널을 통과하며, 츠가루 해협의 아름다운 경치를 감상할 수 있습니다. JR 홋카이도에서 운행하는 홋카이도 신칸센은 하코다테와 신하코다테호쿠토 등 주요 정차지를 거치며 일본 최북단까지 빠르고 편안한 이동 경험을 제공해요. 지금 클룩에서 홋카이도 신칸센 티켓을 예약하고 겨울의 홋카이도를 나만의 속도로 즐겨보세요.",
    },
    {
        "error_type": "MISTRANSLATION",
        "impact_type": "Major",
        "source": 'Shinkansen, commonly known as the "bullet train", is the fastest train in Japan.',
        "target": "일본에서 가장 빠른 고속열차인 신칸센의 최대 시속은 노선에 따라 다릅니다.",
        "offer": "신칸센(일명 '버블 트레인')은 일본에서 가장 빠른 열차입니다.",
        "reason": "원문의 'Shinkansen is the fastest train in Japan'이라는 사실을 '최대 시속은 노선에 따라 다릅니다'로 오역하여 핵심 정보('가장 빠른 열차')가 누락됨. 또한 'bullet train'은 '버블 트레인'으로 직역하는 것이 자연스럽지 않으며, '버블 트레인'보다는 '신칸센'의 별칭으로 통용되는 '버블 트레인'을 적절히 처리해야 함.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": 'Shinkansen, commonly known as the "bullet train", is the fastest train in Japan. These high-speed trains can reach speeds of up to 320 km/h (200 mph) on certain routes. The Nozomi and Mizuho Shinkansen services are among the fastest and most efficient options, connecting major cities like Tokyo, Osaka, and Fukuoka in record time.Other Shinkansen lines, like the Hayabusa and Hokuriku Shinkansen, also offer connections between different regions of Japan, making them a great choice if you\'re looking to reach your destinations quickly.',
        "orig_translation": "일본에서 가장 빠른 고속열차인 신칸센의 최대 시속은 노선에 따라 다릅니다. 일부 신칸센 노선은 최고 속도가 320km/h에 달할 수 있습니다. 특히 노조미와 미즈호 열차는 도쿄, 오사카, 후쿠오카와 같은 주요 도시를 연결하는 가장 빠른 신칸센입니다. 하야부사 및 호쿠리쿠 신칸센 등 다른 신칸센 노선도 일본 각지를 신속하고 간편하게 연결합니다.",
    },
    {
        "error_type": "UNDERTRANSLATION",
        "impact_type": "Minor",
        "source": "The Nozomi and Mizuho Shinkansen services are among the fastest and most efficient options, connecting major cities like Tokyo, Osaka, and Fukuoka in record time.",
        "target": "특히 노조미와 미즈호 열차는 도쿄, 오사카, 후쿠오카와 같은 주요 도시를 연결하는 가장 빠른 신칸센입니다.",
        "offer": "노조미와 미즈호 신칸센은 도쿄, 오사카, 후쿠오카 같은 주요 도시를 기록적인 시간 내에 연결하는 가장 빠르고 효율적인 옵션입니다.",
        "reason": "원문의 'fastest and most efficient options' 및 'in record time'이라는 표현이 '가장 빠른 신칸센'으로만 요약되어 핵심 의미('효율적', '기록적인 시간')가 일부 누락됨.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": 'Shinkansen, commonly known as the "bullet train", is the fastest train in Japan. These high-speed trains can reach speeds of up to 320 km/h (200 mph) on certain routes. The Nozomi and Mizuho Shinkansen services are among the fastest and most efficient options, connecting major cities like Tokyo, Osaka, and Fukuoka in record time.Other Shinkansen lines, like the Hayabusa and Hokuriku Shinkansen, also offer connections between different regions of Japan, making them a great choice if you\'re looking to reach your destinations quickly.',
        "orig_translation": "일본에서 가장 빠른 고속열차인 신칸센의 최대 시속은 노선에 따라 다릅니다. 일부 신칸센 노선은 최고 속도가 320km/h에 달할 수 있습니다. 특히 노조미와 미즈호 열차는 도쿄, 오사카, 후쿠오카와 같은 주요 도시를 연결하는 가장 빠른 신칸센입니다. 하야부사 및 호쿠리쿠 신칸센 등 다른 신칸센 노선도 일본 각지를 신속하고 간편하게 연결합니다.",
    },
    {
        "error_type": "MISTRANSLATION",
        "impact_type": "Minor",
        "source": "Other Shinkansen lines, like the Hayabusa and Hokuriku Shinkansen, also offer connections between different regions of Japan, making them a great choice if you're looking to reach your destinations quickly.",
        "target": "하야부사 및 호쿠리쿠 신칸센 등 다른 신칸센 노선도 일본 각지를 신속하고 간편하게 연결합니다.",
        "offer": "하야부사 및 호쿠리쿠 신칸센 등 다른 신칸센 노선도 일본 각지 간의 연결을 제공하며, 목적지에 빠르게 도착하고 싶은 여행객에게 이상적인 선택입니다.",
        "reason": "원문의 'making them a great choice if you're looking to reach your destinations quickly'라는 조건절이 '신속하고 간편하게 연결합니다'로 간단히 요약되어, 원문의 목적지 도착 속도에 대한 강조와 추천 톤이 약화됨.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": 'Shinkansen, commonly known as the "bullet train", is the fastest train in Japan. These high-speed trains can reach speeds of up to 320 km/h (200 mph) on certain routes. The Nozomi and Mizuho Shinkansen services are among the fastest and most efficient options, connecting major cities like Tokyo, Osaka, and Fukuoka in record time.Other Shinkansen lines, like the Hayabusa and Hokuriku Shinkansen, also offer connections between different regions of Japan, making them a great choice if you\'re looking to reach your destinations quickly.',
        "orig_translation": "일본에서 가장 빠른 고속열차인 신칸센의 최대 시속은 노선에 따라 다릅니다. 일부 신칸센 노선은 최고 속도가 320km/h에 달할 수 있습니다. 특히 노조미와 미즈호 열차는 도쿄, 오사카, 후쿠오카와 같은 주요 도시를 연결하는 가장 빠른 신칸센입니다. 하야부사 및 호쿠리쿠 신칸센 등 다른 신칸센 노선도 일본 각지를 신속하고 간편하게 연결합니다.",
    },
    {
        "error_type": "STYLE GUIDE ISSUE",
        "impact_type": "Minor",
        "source": "320 km/h (200 mph)",
        "target": "320km/h",
        "offer": "320km/h (200mph)",
        "reason": "Klook 스타일 가이드에 따라 단위 표기 시 공백을 포함하고, 원문의 단위 변환 정보(200mph)를 반드시 유지해야 함. 공백 누락 및 원문 정보 누락은 스타일 가이드 위반.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": 'Shinkansen, commonly known as the "bullet train", is the fastest train in Japan. These high-speed trains can reach speeds of up to 320 km/h (200 mph) on certain routes. The Nozomi and Mizuho Shinkansen services are among the fastest and most efficient options, connecting major cities like Tokyo, Osaka, and Fukuoka in record time.Other Shinkansen lines, like the Hayabusa and Hokuriku Shinkansen, also offer connections between different regions of Japan, making them a great choice if you\'re looking to reach your destinations quickly.',
        "orig_translation": "일본에서 가장 빠른 고속열차인 신칸센의 최대 시속은 노선에 따라 다릅니다. 일부 신칸센 노선은 최고 속도가 320km/h에 달할 수 있습니다. 특히 노조미와 미즈호 열차는 도쿄, 오사카, 후쿠오카와 같은 주요 도시를 연결하는 가장 빠른 신칸센입니다. 하야부사 및 호쿠리쿠 신칸센 등 다른 신칸센 노선도 일본 각지를 신속하고 간편하게 연결합니다.",
    },
    {
        "error_type": "UNDERTRANSLATION",
        "impact_type": "Major",
        "source": "to understand any applicable fees or conditions",
        "target": "확인해주세요",
        "offer": "해당 수수료 또는 조건을 이해하기 위해 확인해주세요",
        "reason": "원문의 'to understand any applicable fees or conditions'는 목적을 명확히 전달해야 하며, '확인해주세요'만으로는 핵심 의미('수수료 또는 조건 이해')가 누락됨.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": "The ticket policies for the Shinkansen vary depending on the type of train, seat class, and booking conditions. Be sure to review the ticket cancellation and refund policy before completing your checkout to understand any applicable fees or conditions.",
        "orig_translation": "신칸센 티켓 정책은 열차 종류, 좌석 클래스, 예약 조건에 따라 상이합니다. 예약을 완료하기 전 취소 및 환불 정책을 자세히 확인해주세요.",
    },
    {
        "error_type": "MISTRANSLATION",
        "impact_type": "Major",
        "source": "it's highly recommended, especially during peak travel times or holidays",
        "target": "여행 성수기나 공휴일의 경우 미리 예약하시는 것을 적극 추천드려요.",
        "offer": "성수기나 공휴일에는 특히 좌석을 미리 예약하는 것을 적극 추천합니다.",
        "reason": "원문의 'it's highly recommended'는 '적극 추천합니다'로 자연스럽게 표현해야 하며, '미리 예약하시는 것을 적극 추천드려요'는 문맥과 어울리지 않으며, '미리'라는 부가 정보가 원문에 없어 과도한 정보 추가(overtranslation)가 됨.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": "While it's not mandatory to reserve a seat on all Shinkansen lines, it's highly recommended, especially during peak travel times or holidays. Reserved seats guarantee you a specific seat in designated cars, ensuring a smooth and comfortable journey. Non-reserved seats are available on many trains, but they operate on a first-come, first-served basis.",
        "orig_translation": "모든 신칸센 노선의 좌석을 예약해야 하는 것은 아니지만 여행 성수기나 공휴일의 경우 미리 예약하시는 것을 적극 추천드려요. 좌석을 예약하면 지정 객차의 특정 좌석을 보장해 안심하고 편안하게 여행을 즐길 수 있어요. 많은 열차에서 비지정석을 운영하고 있지만 선착순으로 이용이 가능한 점 참고해주세요.",
    },
    {
        "error_type": "OVERTRANSLATION",
        "impact_type": "Major",
        "source": "Reserved seats guarantee you a specific seat in designated cars",
        "target": "좌석을 예약하면 지정 객차의 특정 좌석을 보장해 안심하고 편안하게 여행을 즐길 수 있어요.",
        "offer": "지정 객차의 특정 좌석을 보장해 줍니다.",
        "reason": "원문은 사실 정보를 전달하는 설명문이지만, '안심하고 편안하게 여행을 즐길 수 있어요'는 원문에 없는 감정적 요소를 추가하여 과도한 번역(overtranslation)이 발생함.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": "While it's not mandatory to reserve a seat on all Shinkansen lines, it's highly recommended, especially during peak travel times or holidays. Reserved seats guarantee you a specific seat in designated cars, ensuring a smooth and comfortable journey. Non-reserved seats are available on many trains, but they operate on a first-come, first-served basis.",
        "orig_translation": "모든 신칸센 노선의 좌석을 예약해야 하는 것은 아니지만 여행 성수기나 공휴일의 경우 미리 예약하시는 것을 적극 추천드려요. 좌석을 예약하면 지정 객차의 특정 좌석을 보장해 안심하고 편안하게 여행을 즐길 수 있어요. 많은 열차에서 비지정석을 운영하고 있지만 선착순으로 이용이 가능한 점 참고해주세요.",
    },
    {
        "error_type": "AWKWARD STYLE & REPETITIONS",
        "impact_type": "Minor",
        "source": "Non-reserved seats are available on many trains, but they operate on a first-come, first-served basis.",
        "target": "많은 열차에서 비지정석을 운영하고 있지만 선착순으로 이용이 가능한 점 참고해주세요.",
        "offer": "많은 열차에서 비지정석을 이용할 수 있지만, 선착순으로 이용됩니다.",
        "reason": "원문의 'but they operate on a first-come, first-served basis'는 단순한 사실 전달이지만, '점 참고해주세요'는 부가적인 조언 어조를 추가하여 어색함. 또한 '비지정석을 운영하고 있지만'이라는 표현은 원문의 'available' 의미를 왜곡함.",
        "key": "contents",
        "item_type": "japan-rail/shinkansen",
        "orig_source": "While it's not mandatory to reserve a seat on all Shinkansen lines, it's highly recommended, especially during peak travel times or holidays. Reserved seats guarantee you a specific seat in designated cars, ensuring a smooth and comfortable journey. Non-reserved seats are available on many trains, but they operate on a first-come, first-served basis.",
        "orig_translation": "모든 신칸센 노선의 좌석을 예약해야 하는 것은 아니지만 여행 성수기나 공휴일의 경우 미리 예약하시는 것을 적극 추천드려요. 좌석을 예약하면 지정 객차의 특정 좌석을 보장해 안심하고 편안하게 여행을 즐길 수 있어요. 많은 열차에서 비지정석을 운영하고 있지만 선착순으로 이용이 가능한 점 참고해주세요.",
    },
]


def to_csv(file_name: str):

    records = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    df = pd.DataFrame(records)
    df = df.rename(
        columns={
            "error_type": "Error type",
            "impact_type": "Impact",
            "source": "Source text",
            "target": "Translated text",
            "reason": "Issue Description",
        }
    )

    df["AID"] = "railway"

    df = df[
        [
            "AID",
            "Source text",
            "Translated text",
            "Issue Description",
            "Error type",
            "Impact",
        ]
    ]

    df.to_csv("workingsheets/records.csv", index=False, header=False)


if __name__ == "__main__":
    to_csv("evaluations/klook_trains_evaluations.jsonl")
