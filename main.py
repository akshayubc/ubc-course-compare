import numpy as np
import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="UBC Course Compare",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
BASE_URL_V1 = "https://raw.githubusercontent.com/DonneyF/ubc-pair-grade-data/1516765eb6fd962066149b18ec8c6d64ae06046a/tableau-dashboard/UBCV"
BASE_URL_V2 = "https://raw.githubusercontent.com/DonneyF/ubc-pair-grade-data/master/tableau-dashboard-v2/UBCV"
YEARS = list(range(2014, 2025))  # Extended to 2024
TERMS = ['W', 'S']  # Winter, Summer
GRADE_RANGES = ['<50', '50-54', '55-59', '60-63', '64-67', '68-71', '72-75', '76-79', '80-84', '85-89', '90-100']

# Course list (cleaned up)
COURSE_CODES = [
    'AANB', 'ACAM', 'ADHE', 'AFST', 'AGEC', 'AMNE', 'ANAT', 'ANTH', 'APBI', 'APPP', 'APSC', 'AQUA', 'ARBC', 'ARBM', 
    'ARC *', 'ARCH', 'ARCL', 'ARST', 'ARTC', 'ARTH', 'ARTS', 'ASIA', 'ASIC', 'ASL', 'ASLA *', 'ASTR', 'ASTU', 'ATSC', 
    'AUDI', 'BA', 'BAAC', 'BABS', 'BAEN', 'BAFI', 'BAHR', 'BAIT', 'BALA', 'BAMA', 'BAMS', 'BAPA', 'BASC', 'BASM', 
    'BAUL', 'BEST', 'BIOC', 'BIOF', 'BIOL', 'BIOT', 'BMEG', 'BOTA', 'BRDG', 'BUSI', 'CAPS', 'CCFI', 'CCST', 'CDST', 
    'CEEN', 'CELL', 'CENS', 'CHBE', 'CHEM', 'CHIL', 'CHIN', 'CIVL', 'CLST *', 'CNPS', 'CNTO', 'COEC', 'COGS', 'COHR', 
    'COLX', 'COMM', 'COMR', 'CONS', 'CPEN', 'CPSC', 'CRWR', 'CSIS', 'CSPW', 'CTLN *', 'DANI', 'DENT', 'DES', 'DHYG', 
    'DMED', 'DSCI', 'ECED', 'ECON', 'ECPS', 'EDCP', 'EDST', 'EDUC', 'EECE', 'ELEC', 'ELI', 'EMBA *', 'ENDS *', 'ENGL', 
    'ENPH', 'ENPP *', 'ENST', 'ENVE', 'ENVR', 'EOSC', 'EPSE', 'ETEC', 'EXCH', 'EXGR', 'FACT *', 'FCOR', 'FEBC', 'FIPR', 
    'FISH', 'FIST', 'FMPR *', 'FMST', 'FNEL', 'FNH', 'FNIS', 'FOOD', 'FOPE', 'FOPR', 'FRE', 'FREN', 'FRSI *', 'FRST', 
    'FSCT', 'GEM', 'GENE', 'GEOG', 'GEOS', 'GERM', 'GREK', 'GRS', 'GRSJ', 'GSAT', 'HEBR', 'HESO *', 'HGSE', 'HINU', 
    'HIST', 'HPB', 'HUNU', 'IAR', 'IEST *', 'IGEN', 'ILS *', 'INDO *', 'INDS', 'INFO', 'INLB', 'ISCI', 'ITAL', 'ITST *', 
    'IWME', 'JAPN', 'JRNL', 'KIN', 'KORN', 'LAIS', 'LARC', 'LASO', 'LAST', 'LATN', 'LAW', 'LFS', 'LIBE', 'LIBR', 'LING', 
    'LLED', 'LWS', 'MANU', 'MATH', 'MDIA *', 'MDVL', 'MECH', 'MEDD', 'MEDG', 'MEDI', 'MES', 'MGMT *', 'MICB', 'MIDW', 
    'MINE', 'MRNE', 'MTRL', 'MUSC', 'NAME', 'NEPL *', 'NEST *', 'NEUR *', 'NRSC', 'NSCI', 'NURS', 'OBMS *', 'OBST', 
    'OHS *', 'ONCO', 'ORNT', 'ORPA', 'OSOT', 'PATH', 'PCTH', 'PERS', 'PHAR', 'PHIL', 'PHRM', 'PHTH', 'PHYL *', 'PHYS', 
    'PLAN', 'PLAS *', 'PLNT', 'POLI', 'POLS', 'PORT', 'PPGA', 'PRHC *', 'PSYC', 'PSYT', 'PUNJ', 'RADI *', 'RADS *', 
    'RELG', 'RES', 'RGLA *', 'RGST', 'RHSC', 'RMST', 'RUSS', 'SANS', 'SCAN', 'SCIE', 'SEAL', 'SGES *', 'SLAV', 'SOAL *', 
    'SOCI', 'SOIL', 'SOWK', 'SPAN', 'SPE', 'SPHA', 'SPPH', 'STAT', 'STS', 'SURG', 'SWED', 'TEST', 'THFL', 'THTR', 'TIBT', 
    'TRSC', 'UDES', 'UFOR', 'UKRN *', 'URO *', 'UROL *', 'URST', 'URSY', 'VANT', 'VGRD', 'VISA', 'VRHC *', 'VURS', 
    'WACH', 'WOOD', 'WRDS', 'WRIT *', 'ZOOL'
]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_course_data(course_code, year, term):
    """Fetch course data from the appropriate GitHub repository with error handling."""
    # Determine which data source to use based on year
    if year >= 2022:
        # Use Tableau Dashboard v2 for 2022 and later
        base_url = BASE_URL_V2
        data_source = "Tableau Dashboard v2"
    else:
        # Use original Tableau Dashboard for 2014-2021
        base_url = BASE_URL_V1
        data_source = "Tableau Dashboard"
    
    try:
        url = f"{base_url}/{year}{term}/UBCV-{year}{term}-{course_code}.csv"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = pd.read_csv(url)
        
        # Add data source info for debugging
        if st.session_state.get('debug_mode', False):
            st.info(f"📊 Data loaded from: {data_source} ({year}{term})")
        
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"❌ **Course Not Found**: It seems like {course_code} may not have existed during {year} {term} semester. Please try a different year, term, or course code.")
        return None
    except Exception as e:
        st.error(f"❌ **Data Loading Error**: Unable to load data for {course_code} {year}{term}. Please try a different combination.")
        return None

def get_grade_distribution_data(data, course_number):
    """Extract grade distribution data for a specific course."""
    if data is None:
        return None
    
    course_data = data[data['Course'] == int(course_number)]
    if course_data.empty:
        return None
    
    # Handle different data structures between v1 and v2
    # v1 has 'OVERALL' sections, v2 doesn't have them
    if 'Section' in course_data.columns:
        overall_data = course_data[course_data['Section'] == 'OVERALL']
        if overall_data.empty:
            # For v2 data without OVERALL sections, use all sections combined
            overall_data = course_data
    else:
        # For v2 data, use all available data
        overall_data = course_data
    
    if overall_data.empty:
        return None
    
    grade_dist = {}
    for grade_range in GRADE_RANGES:
        if grade_range in overall_data.columns:
            # Sum across all sections if multiple sections exist
            grade_dist[grade_range] = overall_data[grade_range].sum() if len(overall_data) > 1 else overall_data[grade_range].iloc[0]
        else:
            grade_dist[grade_range] = 0
    
    return grade_dist

def create_comparison_chart(data1, data2, course1_name, course2_name):
    """Create an interactive comparison chart using Plotly."""
    if data1 is None or data2 is None:
        return None
    
    fig = go.Figure()
    
    # Add course 1 data
    fig.add_trace(go.Scatter(
        x=GRADE_RANGES,
        y=list(data1.values()),
        mode='lines+markers',
        name=course1_name,
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # Add course 2 data
    fig.add_trace(go.Scatter(
        x=GRADE_RANGES,
        y=list(data2.values()),
        mode='lines+markers',
        name=course2_name,
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Grade Distribution Comparison",
        xaxis_title="Grade Range",
        yaxis_title="Number of Students",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

def calculate_summary_stats(data):
    """Calculate summary statistics for course data."""
    if data is None:
        return None
    
    stats = {}
    for grade_range in GRADE_RANGES:
        if grade_range in data:
            stats[grade_range] = data[grade_range]
    
    total_students = sum(stats.values())
    if total_students > 0:
        # Calculate percentage distribution
        stats_pct = {k: (v/total_students)*100 for k, v in stats.items()}
        return {
            'total_students': total_students,
            'distribution': stats,
            'distribution_pct': stats_pct
        }
    return None

def calculate_grade_statistics(data, course_number):
    """Calculate average and median grades for a course."""
    if data is None:
        return None
    
    course_data = data[data['Course'] == int(course_number)]
    if course_data.empty:
        return None
    
    # Handle different data structures between v1 and v2
    if 'Section' in course_data.columns:
        overall_data = course_data[course_data['Section'] == 'OVERALL']
        if overall_data.empty:
            overall_data = course_data
    else:
        overall_data = course_data
    
    if overall_data.empty:
        return None
    
    # Get average and median if available
    avg_grade = None
    median_grade = None
    instructor_name = None
    
    # Debug: Print available columns
    if st.session_state.get('debug_mode', False):
        st.write(f"Available columns: {list(overall_data.columns)}")
    
    # Try different possible column names for average
    for col in ['Avg', 'Average', 'Mean', 'avg', 'average']:
        if col in overall_data.columns:
            avg_grade = overall_data[col].iloc[0] if not overall_data.empty else None
            break
    
    # Try different possible column names for median
    for col in ['Median', 'median', 'Med']:
        if col in overall_data.columns:
            median_grade = overall_data[col].iloc[0] if not overall_data.empty else None
            break
    
    # Try different possible column names for instructor
    for col in ['Instructor', 'Instructor Name', 'Professor', 'instructor', 'professor']:
        if col in overall_data.columns:
            instructor_name = overall_data[col].iloc[0] if not overall_data.empty else None
            break
    
    return {
        'average': avg_grade,
        'median': median_grade,
        'instructor': instructor_name
    }

def main():
    # Header
    st.title("🎓 UBC Course Compare")
    st.markdown("Compare UBC courses by analyzing grade distributions, averages, and other metrics across different years, semesters, and professors.")
    
    # Data source information
    with st.expander("📊 Data Sources & Coverage"):
        st.markdown("""
        **Data Coverage:**
        - **2014-2021**: Tableau Dashboard (Original)
        - **2022-2024**: Tableau Dashboard v2 (Latest)
        
        **Data Sources:**
        - [UBC PAIR Grade Distribution Data](https://github.com/DonneyF/ubc-pair-grade-data)
        - Updated regularly with new semester data
        
        **Note**: Data structure changed in 2022, but the app automatically handles both formats.
        """)
    
    # # Debug mode toggle
    # debug_mode = st.sidebar.checkbox("🔧 Debug Mode", help="Show additional debugging information")
    # if debug_mode:
    #     st.session_state['debug_mode'] = True
    # else:
    #     st.session_state['debug_mode'] = False
    
    # Sidebar
    st.sidebar.header("📚 Course Selection")
    st.sidebar.markdown("Select two courses to compare:")
    
    # Course 1 Selection
    st.sidebar.subheader("Course 1")
    course1_code = st.sidebar.selectbox(
        "Course Code",
        COURSE_CODES,
        index=COURSE_CODES.index('CPSC'),  # Default to CPSC
        key="course1_code",
        help="Select the course code (e.g., MATH, CPSC, COMM)"
    )
    
    year1 = st.sidebar.selectbox(
        "Year",
        YEARS,
        index=YEARS.index(2019),  # Default to 2019
        key="year1",
        help="Data available from 2014-2024"
    )
    
    term1 = st.sidebar.selectbox(
        "Term",
        TERMS,
        format_func=lambda x: "Winter" if x == "W" else "Summer",
        key="term1"
    )
    
    # Fetch and display course 1 data
    with st.spinner(f"Loading {course1_code} data..."):
        course1_data = fetch_course_data(course1_code, year1, term1)
    
    if course1_data is not None:
        course1_numbers = sorted(course1_data['Course'].unique())
        # Default to 110 if available, otherwise first available course
        default_course1_index = 0
        if 110 in course1_numbers:
            default_course1_index = course1_numbers.index(110)
        
        course1_number = st.sidebar.selectbox(
            "Course Number",
            course1_numbers,
            index=default_course1_index,
            key="course1_number"
        )
    else:
        st.sidebar.error(f"No data available for {course1_code} {year1}{term1}")
        course1_number = None
    
    # Course 2 Selection
    st.sidebar.subheader("Course 2")
    course2_code = st.sidebar.selectbox(
        "Course Code",
        COURSE_CODES,
        index=COURSE_CODES.index('CPSC'),  # Default to CPSC
        key="course2_code",
        help="Select the course code (e.g., MATH, CPSC, COMM)"
    )
    
    year2 = st.sidebar.selectbox(
        "Year",
        YEARS,
        index=YEARS.index(2020),  # Default to 2020
        key="year2",
        help="Data available from 2014-2024"
    )
    
    term2 = st.sidebar.selectbox(
        "Term",
        TERMS,
        format_func=lambda x: "Winter" if x == "W" else "Summer",
        key="term2"
    )
    
    # Fetch and display course 2 data
    with st.spinner(f"Loading {course2_code} data..."):
        course2_data = fetch_course_data(course2_code, year2, term2)
    
    if course2_data is not None:
        course2_numbers = sorted(course2_data['Course'].unique())
        # Default to 110 if available, otherwise first available course
        default_course2_index = 0
        if 110 in course2_numbers:
            default_course2_index = course2_numbers.index(110)
        
        course2_number = st.sidebar.selectbox(
            "Course Number",
            course2_numbers,
            index=default_course2_index,
            key="course2_number"
        )
    else:
        st.sidebar.error(f"No data available for {course2_code} {year2}{term2}")
        course2_number = None
    
    # Main content area
    if course1_number and course2_number:
        # Create proper course labels with year and term
        course1_label = f"{course1_code} {course1_number} {year1} {term1}"
        course2_label = f"{course2_code} {course2_number} {year2} {term2}"
        
        st.header(f"📊  Comparing {course1_label} vs {course2_label}")
        
        # Get grade distribution data
        grade_dist1 = get_grade_distribution_data(course1_data, course1_number)
        grade_dist2 = get_grade_distribution_data(course2_data, course2_number)
        
        if grade_dist1 and grade_dist2:
            # Create comparison chart
            fig = create_comparison_chart(
                grade_dist1, grade_dist2,
                course1_label,
                course2_label
            )
            
            if fig:
                st.plotly_chart(fig, width='stretch')
            
            # Summary statistics
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(f"📈 {course1_label} Summary")
                stats1 = calculate_summary_stats(grade_dist1)
                grade_stats1 = calculate_grade_statistics(course1_data, course1_number)
                
                if stats1:
                    st.metric("Total Students", f"{stats1['total_students']:,}")
                    
                    # Add grade statistics
                    if grade_stats1:
                        if grade_stats1['average'] is not None:
                            st.metric("Average Grade", f"{grade_stats1['average']:.1f}%")
                        else:
                            st.metric("Average Grade", "N/A")
                        
                        if grade_stats1['median'] is not None:
                            st.metric("Median Grade", f"{grade_stats1['median']:.1f}%")
                        else:
                            st.metric("Median Grade", "N/A")
                        
                        if grade_stats1['instructor'] is not None:
                            st.metric("Instructor", grade_stats1['instructor'])
                        else:
                            st.metric("Instructor", "N/A")
                    else:
                        st.metric("Average Grade", "N/A")
                        st.metric("Median Grade", "N/A")
                        st.metric("Instructor", "N/A")
                    
                    # Grade distribution table
                    dist_df1 = pd.DataFrame(list(stats1['distribution_pct'].items()), 
                                          columns=['Grade Range', 'Percentage'])
                    st.dataframe(dist_df1, width='stretch')
            
            with col2:
                st.subheader(f"📈 {course2_label} Summary")
                stats2 = calculate_summary_stats(grade_dist2)
                grade_stats2 = calculate_grade_statistics(course2_data, course2_number)
                
                if stats2:
                    st.metric("Total Students", f"{stats2['total_students']:,}")
                    
                    # Add grade statistics
                    if grade_stats2:
                        if grade_stats2['average'] is not None:
                            st.metric("Average Grade", f"{grade_stats2['average']:.1f}%")
                        else:
                            st.metric("Average Grade", "N/A")
                        
                        if grade_stats2['median'] is not None:
                            st.metric("Median Grade", f"{grade_stats2['median']:.1f}%")
                        else:
                            st.metric("Median Grade", "N/A")
                        
                        if grade_stats2['instructor'] is not None:
                            st.metric("Instructor", grade_stats2['instructor'])
                        else:
                            st.metric("Instructor", "N/A")
                    else:
                        st.metric("Average Grade", "N/A")
                        st.metric("Median Grade", "N/A")
                        st.metric("Instructor", "N/A")
                    
                    # Grade distribution table
                    dist_df2 = pd.DataFrame(list(stats2['distribution_pct'].items()), 
                                          columns=['Grade Range', 'Percentage'])
                    st.dataframe(dist_df2, width='stretch')
            
            # Detailed comparison
            st.subheader("🔍 Detailed Comparison")
            
            # Create comparison table
            comparison_data = []
            for grade_range in GRADE_RANGES:
                if grade_range in grade_dist1 and grade_range in grade_dist2:
                    comparison_data.append({
                        'Grade Range': grade_range,
                        course1_label: grade_dist1[grade_range],
                        course2_label: grade_dist2[grade_range],
                        'Difference': grade_dist1[grade_range] - grade_dist2[grade_range]
                    })
            
            if comparison_data:
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, width='stretch')
        
        else:
            st.error("Unable to load grade distribution data for one or both courses.")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Need help?**")
    st.sidebar.markdown("Contact: akshay.ubcv@gmail.com")
    st.sidebar.markdown("**Data Source:** [UBC PAIR Grade Distribution](https://github.com/DonneyF/ubc-pair-grade-data)")
    st.sidebar.markdown("**Coverage:** 2014-2024")
    
    # Instructions
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        ### How to Compare Courses:
        
        1. **Select Course 1**: Choose the course code, year, term, and course number
        2. **Select Course 2**: Choose the second course to compare
        3. **View Results**: The app will show:
           - Interactive grade distribution charts
           - Summary statistics for each course
           - Detailed comparison tables
        
        ### Tips:
        - Compare the same course across different years to see grade trends
        - Compare different courses in the same term to see relative difficulty
        - Use the charts to identify grade distribution patterns
        - Check the summary statistics for enrollment numbers
        """)

if __name__ == "__main__":
    main()
