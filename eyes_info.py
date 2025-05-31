import pandas as pd

class EyesProduct:
    def __init__(self, clean_name, summary, url):
        self.clean_name = clean_name
        self.summary = summary
        self.url = url

    def __repr__(self):
        return f"EyesProduct(clean_name='{self.clean_name}', summary='{self.summary}', url='{self.url}')"

def search(code):
    df = pd.read_csv('EYES_analysis_final_cleaned.csv')
    df_filtered = df[df['EYES_code'] == code][['clean_name', 'summary', 'url']]
    # url을 markdown 하이퍼링크로 변환
    df_filtered['url'] = df_filtered['url'].apply(lambda x: f"[바로가기]({x})" if pd.notna(x) else "")

    # 칼럼명 변경
    df_filtered = df_filtered.rename(columns={
        'clean_name': '상품명',
        'summary': '후기',
        'url': '링크'
    })
    return df_filtered
