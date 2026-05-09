# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'cloud-deployment')
from static_translations import get_static_answer, get_operating_hours_text

results = []
results.append(('parking_KR', bool(get_static_answer('parking', '한국어', '청소년/성인'))))
results.append(('parking_EN', bool(get_static_answer('parking', 'English', '청소년/성인'))))
results.append(('parking_KR_kid', bool(get_static_answer('parking', '한국어', '어린이'))))
results.append(('admission_JP', bool(get_static_answer('admission_fee', '日本語', '청소년/성인'))))
results.append(('floor_ZH', bool(get_static_answer('floor_guide', '中文', '청소년/성인'))))
results.append(('today_programs_none', get_static_answer('today_programs', 'English', '청소년/성인')))
results.append(('op_hours_EN_open', bool(get_operating_hours_text('English', '청소년/성인', '현재 정상 운영 중입니다! 관람시간은 09:30~17:30이고, 입장 마감은 16:30이에요.'))))
results.append(('op_hours_JP_closed_mon', bool(get_operating_hours_text('日本語', '청소년/성인', '04월 28일(월요일)은 정기휴관일(월요일)입니다.'))))

with open('_smoke_result.txt', 'w', encoding='utf-8') as f:
    for k, v in results:
        f.write(f'{k}: {v}\n')

print('done')
