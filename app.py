from flask import Flask, render_template
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import os

app = Flask(__name__)

def data_handling(path):
    df2 = pd.read_json(path)
    vote_ratioss = df2[df2['İl Id'].str.contains('Oy Oranı')].copy()
    ince = vote_ratioss['İl Adı'].tolist()
    ince = [item.strip() for item in ince]
    aksener = vote_ratioss['Kayıtlı Seçmen Sayısı'].tolist()
    aksener = [item.strip() for item in aksener]
    rte = vote_ratioss['Oy Kullanan Seçmen Sayısı'].tolist()
    rte = [item.strip() for item in rte]
    demirtas = vote_ratioss['Geçerli Oy Toplamı'].tolist()
    demirtas = [item.strip() for item in demirtas]
    temel = vote_ratioss[' MUHARREM İNCE '].tolist()
    temel = [item.strip() for item in temel]
    perincek = vote_ratioss[' MERAL AKŞENER '].tolist()
    perincek = [item.strip() for item in perincek]
    df = df2[~df2['İl Id'].str.contains('Oy Oranı')]
    df = df.reset_index(drop=True)
    df1 = df.replace('', pd.NA)
    numeric_columns = ['Kayıtlı Seçmen Sayısı', 'Oy Kullanan Seçmen Sayısı', 'Geçerli Oy Toplamı']
    for col in numeric_columns:
        df1[col] = df1[col].str.replace('.', '').str.replace(' ', '').str.strip().astype(float)
    df1['Geçersiz Oy Toplamı'] = df1['Oy Kullanan Seçmen Sayısı'] - df1['Geçerli Oy Toplamı']
    sum_columns = ['Kayıtlı Seçmen Sayısı', 'Oy Kullanan Seçmen Sayısı', 'Geçerli Oy Toplamı', 'Geçersiz Oy Toplamı']
    totals = pd.DataFrame(df1[sum_columns].sum()).transpose()  
    df1[" MUHARREM İNCE "] = df1[" MUHARREM İNCE "].str.replace('.', '').str.replace(' ', '').str.strip().astype(float)
    df1[" MERAL AKŞENER "] = df1[" MERAL AKŞENER "].str.replace('.', '').str.replace(' ', '').str.strip().astype(float)
    df1[" RECEP TAYYİP ERDOĞAN "] = df1[" RECEP TAYYİP ERDOĞAN "].str.replace('.', '').str.replace(' ', '').str.strip().astype(float)
    df1[" SELAHATTİN DEMİRTAŞ "] = df1[" SELAHATTİN DEMİRTAŞ "].str.replace('.', '').str.replace(' ', '').str.strip().astype(float)
    df1[" TEMEL KARAMOLLAOĞLU "] = df1[" TEMEL KARAMOLLAOĞLU "].str.replace('.', '').str.replace(' ', '').str.strip().astype(float)
    df1[" DOĞU PERİNÇEK "] = df1[" DOĞU PERİNÇEK "].str.replace('.', '').str.replace(' ', '').str.strip().astype(float)  
    candicate_list = [' MUHARREM İNCE ',' MERAL AKŞENER ',' RECEP TAYYİP ERDOĞAN ',' SELAHATTİN DEMİRTAŞ ',' TEMEL KARAMOLLAOĞLU ',' DOĞU PERİNÇEK ']
    vote_ratios = [round((((df1[' MUHARREM İNCE '].sum() / totals['Geçerli Oy Toplamı'])*100)[0]),2),round(((df1[' MERAL AKŞENER '].sum() / totals['Geçerli Oy Toplamı'])*100)[0],2),round((((df1[' RECEP TAYYİP ERDOĞAN '].sum() / totals['Geçerli Oy Toplamı'])*100)[0]),2),round((((df1[' SELAHATTİN DEMİRTAŞ '].sum() / totals['Geçerli Oy Toplamı'])*100)[0]),2),round((((df1[' TEMEL KARAMOLLAOĞLU '].sum() / totals['Geçerli Oy Toplamı'])*100)[0]),2),round((((df1[' DOĞU PERİNÇEK '].sum() / totals['Geçerli Oy Toplamı'])*100)[0]),2)]
    vote_numbers_str = ["{:,.1f}".format(df1[' MUHARREM İNCE '].sum()),"{:,.1f}".format(df1[' MERAL AKŞENER '].sum()),"{:,.1f}".format(df1[' RECEP TAYYİP ERDOĞAN '].sum()),"{:,.1f}".format(df1[' SELAHATTİN DEMİRTAŞ '].sum()),"{:,.1f}".format(df1[' TEMEL KARAMOLLAOĞLU '].sum()),"{:,.1f}".format(df1[' DOĞU PERİNÇEK '].sum())]
    vote_numbers = [(df1[' MUHARREM İNCE '].sum()),(df1[' MERAL AKŞENER '].sum()),(df1[' RECEP TAYYİP ERDOĞAN '].sum()),(df1[' SELAHATTİN DEMİRTAŞ '].sum()),(df1[' TEMEL KARAMOLLAOĞLU '].sum()),(df1[' DOĞU PERİNÇEK '].sum())]
    data = {'Candicates': candicate_list, 'Vote Ratios': vote_ratios, 'Vote Numbers(formatted)': vote_numbers_str,'Vote Numbers': vote_numbers}
    candicates_ratio = pd.DataFrame(data)
    vote_ratios_last = pd.DataFrame({'Il ID':df1['İl Id'],'MUHARREM İNCE':ince,'MERAL AKŞENER':aksener,'RECEP TAYYİP ERDOĞAN':rte,'SELAHATTİN DEMİRTAŞ':demirtas,'TEMEL KARAMOLLAOĞLU': temel,'DOĞU PERİNÇEK':perincek})
    totals = totals.applymap("{:,.0f}".format)
    return totals, df1,candicates_ratio,vote_ratios_last,df2


def fetch():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    link = "https://acikveri.ysk.gov.tr/anasayfa"
    browser.get(link)
    

@app.route("/")
def anasayfa():
    json_path = os.getcwd()+"/JSON" # Replace with the desired path to save the JSON file
    voters_data, df,candicates_ratios, vote_ratio,df2 = data_handling(json_path+"/IlSonuc/SecimSonucIl.json")
    fm_df = pd.read_json(os.getcwd()+"/JSON/FemaleMaleJSON/femaleMale.json")
    vote_ratio_json = vote_ratio.to_json(orient="records")

    return render_template("index.html",
                           female=fm_df.loc[0][0],
                           male=fm_df.loc[0][1],
                           voters_data = voters_data,
                           df = df,
                           candicates_ratios=candicates_ratios,
                           vote_ratio=vote_ratio,
                           vote_ratio_html=vote_ratio.to_html(),
                           df_html = df.to_html(),
                           vote_ratio_json=vote_ratio_json,
                           df2 = df2.to_html())

if __name__ == "__main__":
    app.run(debug=True)
