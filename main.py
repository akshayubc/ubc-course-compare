
import numpy as np
import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt

st.header("UBC Course Compare")
url = "https://raw.githubusercontent.com/DonneyF/ubc-pair-grade-data/1516765eb6fd962066149b18ec8c6d64ae06046a/tableau-dashboard/UBCV"
url2 = "https://raw.githubusercontent.com/DonneyF/ubc-pair-grade-data/1516765eb6fd962066149b18ec8c6d64ae06046a/tableau-dashboard/UBCV"

course_list = ['AANB','ACAM','ADHE','AFST','AGEC','AMNE','ANAT','ANTH','APBI','APPP','APSC','AQUA','ARBC','ARBM','ARC *','ARCH','ARCL','ARST','ARTC','ARTH','ARTS','ASIA','ASIC','ASL','ASLA *','ASTR','ASTU','ATSC','AUDI','BA','BAAC','BABS','BAEN','BAFI','BAHR','BAIT','BALA','BAMA','BAMS','BAPA','BASC','BASM','BAUL','BEST','BIOC','BIOF','BIOL','BIOT','BMEG','BOTA','BRDG','BUSI','CAPS','CCFI','CCST','CDST','CEEN','CELL','CENS','CHBE','CHEM','CHIL','CHIN','CIVL','CLST *','CNPS','CNTO','COEC','COGS','COHR','COLX','COMM','COMR','CONS','CPEN','CPSC','CRWR','CSIS','CSPW','CTLN *','DANI','DENT','DES','DHYG','DMED','DSCI','ECED','ECON','ECPS','EDCP','EDST','EDUC','EECE','ELEC','ELI','EMBA *','ENDS *','ENGL','ENPH','ENPP *','ENST','ENVE','ENVR','EOSC','EPSE','ETEC','EXCH','EXGR','FACT *','FCOR','FEBC','FIPR','FISH','FIST','FMPR *','FMST','FNEL','FNH','FNIS','FOOD','FOPE','FOPR','FRE','FREN','FRSI *','FRST','FSCT','GEM','GENE','GEOG','GEOS','GERM','GREK','GRS','GRSJ','GSAT','HEBR','HESO *','HGSE','HINU','HIST','HPB','HUNU','IAR','IEST *','IGEN','ILS *','INDO *','INDS','INFO','INLB','ISCI','ITAL','ITST *','IWME','JAPN','JRNL','KIN','KORN','LAIS','LARC','LASO','LAST','LATN','LAW','LFS','LIBE','LIBR','LING','LLED','LWS','MANU','MATH','MDIA *','MDVL','MECH','MEDD','MEDG','MEDI','MES','MGMT *','MICB','MIDW','MINE','MRNE','MTRL','MUSC','NAME','NEPL *','NEST *','NEUR *','NRSC','NSCI','NURS','OBMS *','OBST','OHS *','ONCO','ORNT','ORPA','OSOT','PATH','PCTH','PERS','PHAR','PHIL','PHRM','PHTH','PHYL *','PHYS','PLAN','PLAS *','PLNT','POLI','POLS','PORT','PPGA','PRHC *','PSYC','PSYT','PUNJ','RADI *','RADS *','RELG','RES','RGLA *','RGST','RHSC','RMST','RUSS','SANS','SCAN','SCIE','SEAL','SGES *','SLAV','SOAL *','SOCI','SOIL','SOWK','SPAN','SPE','SPHA','SPPH','STAT','STS','SURG','SWED','TEST','THFL','THTR','TIBT','TRSC','UDES','UFOR','UKRN *','URO *','UROL *','URST','URSY','VANT','VGRD','VISA','VRHC *','VURS','WACH','WOOD','WRDS','WRIT *','ZOOL']

st.sidebar.header("Enter the courses you wish to compare")
st.sidebar.caption('Compare courses from 2014 to 2020')

cc1 = st.sidebar.selectbox(
    "Enter Course Code (for eg: MATH)",
    course_list, 71    )

year1 = st.sidebar.selectbox(
     'Enter year for Course 1',
     (list(range(2014, 2022))), 7)

term1 = st.sidebar.radio(
     "Select Term for Course 1:  Summer (S), Winter (W)",
     ('S', 'W'))
url = url + '/' + str(year1) + str(term1) +"/" 
url = url + "UBCV-" + str(year1) + str(term1) +"-" + cc1 +".csv"
course_num1 = pd.read_csv(url)
course_number_set1 = set(course_num1["Course"])

cn1 = st.sidebar.selectbox(
    "Enter of Course Number (for eg: 221, 121 etc)",
    course_number_set1 
    )

load_data1 = course_num1[(course_num1['Course'] == int(cn1))]
load_data1 = load_data1.drop(['Detail'], axis =1)
# ,'<50','50-54','55-59','60-63', '64-67','68-71', '72-75', '76-79', '80-84', '85-89','90-100'
st.write(load_data1.set_index('Campus'))


cc2 = st.sidebar.selectbox(
    "Enter Course name (for eg: COMM)",
    course_list, 75
    )

year2 = st.sidebar.selectbox(
     'Enter year for Course 2',
     (list(range(2014, 2021))),6)

term2 = st.sidebar.radio(
     "Select Term for Course 2:  Summer (S), Winter (W)",
     ('S', 'W'))

url2 = url2 + '/' + str(year2) + str(term2) +"/" 
url2 = url2 + "UBCV-" + str(year2) + str(term2) +"-" + cc2 +".csv"
course_num2 = pd.read_csv(url2)
course_number_set2 = set(course_num2["Course"])

cn2 = st.sidebar.selectbox(
    "Enter Course Number 2 (for eg: 221, 121 etc)",
    course_number_set2
    )
st.write("Comparing " + cc1 + str(cn1) + " with " + cc2  + str(cn2))

load_data2 = course_num2[(course_num2['Course'] == int(cn2))]
load_data2 = load_data2.drop('Detail', axis = 1)
st.write(load_data2.set_index('Campus'))
st.sidebar.caption('Having issues? Contact akshay.exun@gmail.com')

#Summary Stats
# prof_list = load_data1['Professor']
# avg_list = load_data1['Avg']
# summary_stats = pd.DataFrame(prof_list, avg_list)
# st.write(summary_stats)

# Matplotlib graphing grading trend

x =  ['<50','50-54','55-59','60-63', '64-67','68-71', '72-75', '76-79', '80-84', '85-89','90-100']
y =[]
i=0
overall1 = load_data1[(load_data1['Section'] == 'OVERALL')]
overall2 = load_data2[(load_data2['Section']== 'OVERALL')]

y1 = overall1['<50']
y1= dict(y1)
y2 = overall1[(x[1])]
y2 = dict(y2)
y3 = overall1[x[2]]
y3= dict(y3)
y4 = overall1[(x[3])]
y4 = dict(y4)
y5 = overall1[(x[4])]
y5 = dict(y5)
y6 = overall1[x[5]]
y6= dict(y6)
y7 = overall1[(x[6])]
y7 = dict(y7)
y8 = overall1[(x[7])]
y8 = dict(y8)
y9 = overall1[(x[8])]
y9 = dict(y9)
y10 = overall1[(x[9])]
y10 = dict(y10)
y11 = overall1[(x[10])]
y11 = dict(y11)

y21 = overall2['<50']
y21= dict(y21)
y22 = overall2[(x[1])]
y22 = dict(y22)
y23 = overall2[x[2]]
y23= dict(y23)
y24 = overall2[(x[3])]
y24 = dict(y24)
y25 = overall2[(x[4])]
y25 = dict(y25)
y26 = overall2[x[5]]
y26= dict(y26)
y27 = overall2[(x[6])]
y27 = dict(y27)
y28 = overall2[(x[7])]
y28 = dict(y28)
y29 = overall2[(x[8])]
y29 = dict(y29)
y30 = overall2[(x[9])]
y30 = dict(y30)
y31 = overall2[(x[10])]
y31 = dict(y31)

overall1 = pd.DataFrame(overall1)

y_c1 = [y1.values(),y2.values(),y3.values(),y4.values(),y5.values(),y6.values(),y7.values(),y8.values(),y9.values(),y10.values(),y11.values()]
y_c2 = [y21.values(),y22.values(),y23.values(),y24.values(),y25.values(),y26.values(),y27.values(),y28.values(),y29.values(),y30.values(),y31.values()]
chart_data = pd.DataFrame(
 y_c1, x[:len(x):1], 
#plt.ylabel("Number of Students"),
# plt.title(overall1['Title'])
)

chart_data2 = pd.DataFrame(
    y_c2, x
)
st.subheader("Grade Distribution for " + cc1 + str(cn1) + ":")
st.line_chart(chart_data)
st.line_chart(chart_data2)

st.caption("Made by Akshay Khandelwal")




