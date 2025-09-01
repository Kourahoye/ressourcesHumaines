from workalendar.core import WesternCalendar
from hijri_converter import convert
from datetime import date

class GuineaCalendar(WesternCalendar):
    WEEKEND_DAYS = (6, 7)

    FIXED_HOLIDAYS = WesternCalendar.FIXED_HOLIDAYS + (
        (1, 1, "Jour de l'An"),
        (3, 8, "Journée internationale des droits des femmes"),
        (4, 3, "Fête de l'Indépendance"),
        (5, 1, "Fête du Travail"),
        (10, 2, "Fête nationale"),
        (12, 25, "Noël"),
    )

    def get_variable_days(self, year):
        days = super().get_variable_days(year)

        # Approximation : l'année hijri commence environ 579 ans avant l'année grégorienne
        hijri_year = year - 579

        def hijri_to_gregorian(h_year, h_month, h_day):
            try:
                g_date = convert.Hijri(h_year, h_month, h_day).to_gregorian()
                return date(g_date.year, g_date.month, g_date.day)
            except Exception:
                return None

        # Dates approximatives des fêtes musulmanes
        eid_al_fitr = hijri_to_gregorian(hijri_year, 10, 1)   # 1er Shawwal
        eid_al_adha = hijri_to_gregorian(hijri_year, 12, 10)  # 10 Dhou al-Hijja
        mawlid = hijri_to_gregorian(hijri_year, 3, 12)        # 12 Rabi' al-awwal

        if eid_al_fitr:
            days.append((eid_al_fitr, "Aïd el-Fitr"))
        if eid_al_adha:
            days.append((eid_al_adha, "Aïd al-Adha (Tabaski)"))
        if mawlid:
            days.append((mawlid, "Mawlid (Naissance du Prophète)"))

        return days
