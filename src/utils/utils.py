import dateparser
from datetime import datetime

def dt_ref_to_isodt(txt_dt):
    data_referencia = datetime.now()

    data = dateparser.parse(
        txt_dt,
        languages=['pt'],
        settings={'RELATIVE_BASE': data_referencia}
    )

    if data:
        return data.date().isoformat()
    else:
        return '0000-00-00'