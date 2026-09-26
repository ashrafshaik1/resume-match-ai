import os
import tempfile
import streamlit as st

from parser import extract_text_from_pdf, extract_text_from_docx
from matcher import extract_skills, compare_skills


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Resume Match AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 5%,
                rgba(139, 92, 246, 0.15),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 25%,
                rgba(168, 85, 247, 0.12),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(192, 132, 252, 0.07),
                transparent 35%
            ),
            #0b0d14;
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 45px;
        padding-bottom: 100px;
    }

    * {
        box-sizing: border-box;
    }


    /* =====================================================
       SCROLL REVEAL
       ===================================================== */

    @keyframes scrollReveal {

        from {
            opacity: 0;
            transform:
                translateY(50px)
                scale(0.96)
                rotateX(5deg);
        }

        to {
            opacity: 1;
            transform:
                translateY(0)
                scale(1)
                rotateX(0deg);
        }
    }

    .scroll-reveal {
        animation: scrollReveal 0.9s ease both;
        animation-timeline: view();
        animation-range: entry 0% cover 30%;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        text-align: center;
        padding: 20px 20px 55px 20px;
        animation: heroAppear 1s ease-out;
    }

    @keyframes heroAppear {

        from {
            opacity: 0;
            transform:
                translateY(-25px)
                scale(0.97);
        }

        to {
            opacity: 1;
            transform:
                translateY(0)
                scale(1);
        }
    }

    .brand-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        margin-bottom: 12px;
    }

    .brand-icon {
        width: 62px;
        height: 62px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 19px;

        background:
            linear-gradient(
                135deg,
                #6d28d9,
                #8b5cf6,
                #c084fc
            );

        box-shadow:
            0 0 25px rgba(139, 92, 246, 0.45),
            0 0 70px rgba(168, 85, 247, 0.20);

        transition:
            transform 0.35s ease,
            box-shadow 0.35s ease;
    }

    .brand-icon:hover {
        transform:
            rotate(5deg)
            scale(1.10);

        box-shadow:
            0 0 35px rgba(139, 92, 246, 0.65),
            0 0 90px rgba(168, 85, 247, 0.30);
    }

    .brand-icon svg {
        width: 34px;
        height: 34px;

        fill: none;
        stroke: white;
        stroke-width: 1.8;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .main-title {
        font-size: 46px;
        font-weight: 750;
        letter-spacing: -1.5px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #ddd6fe,
                #c084fc
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #aaa7b8;
        margin-top: 8px;
    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        font-size: 25px;
        font-weight: 650;
        margin-top: 30px;
        margin-bottom: 15px;

        color: #f5f3ff;
        letter-spacing: -0.3px;
    }

    .section-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;

        width: 34px;
        height: 34px;

        margin-right: 10px;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                #6d28d9,
                #a855f7
            );

        color: white;

        font-size: 14px;
        font-weight: 700;

        box-shadow:
            0 5px 20px
            rgba(124, 58, 237, 0.35);

        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }

    .section-number:hover {
        transform: scale(1.10) rotate(5deg);

        box-shadow:
            0 8px 28px
            rgba(168, 85, 247, 0.45);
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {
        border-radius: 17px;
        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }

    [data-testid="stFileUploader"]:hover {
        transform: translateY(-4px);

        box-shadow:
            0 15px 45px
            rgba(139, 92, 246, 0.18);
    }

    [data-testid="stFileUploader"] section {
        border:
            1px dashed
            rgba(168, 85, 247, 0.50);

        background:
            linear-gradient(
                145deg,
                rgba(139, 92, 246, 0.09),
                rgba(30, 27, 46, 0.60)
            );

        border-radius: 17px;
    }


    /* =====================================================
       TEXT AREA
       ===================================================== */

    textarea {
        border-radius: 15px !important;

        background:
            rgba(30, 30, 43, 0.88) !important;

        border:
            1px solid
            rgba(168, 85, 247, 0.28) !important;

        transition:
            border 0.3s ease,
            box-shadow 0.3s ease,
            transform 0.3s ease !important;
    }

    textarea:hover {
        border-color:
            rgba(192, 132, 252, 0.50) !important;
    }

    textarea:focus {
        border:
            1px solid
            rgba(192, 132, 252, 0.85) !important;

        box-shadow:
            0 0 0 2px
            rgba(168, 85, 247, 0.12),
            0 12px 35px
            rgba(139, 92, 246, 0.15) !important;

        transform: translateY(-2px);
    }


    /* =====================================================
       ANALYZE BUTTON
       ===================================================== */

    .stButton > button {
        min-height: 54px;

        border-radius: 14px;

        border:
            1px solid
            rgba(216, 180, 254, 0.45);

        background:
            linear-gradient(
                135deg,
                #6d28d9,
                #8b5cf6,
                #a855f7
            );

        color: white;

        font-size: 17px;
        font-weight: 650;

        box-shadow:
            0 10px 35px
            rgba(124, 58, 237, 0.30);

        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease,
            border-color 0.3s ease;
    }

    .stButton > button:hover {
        transform:
            translateY(-4px)
            scale(1.01);

        box-shadow:
            0 16px 45px
            rgba(168, 85, 247, 0.45);

        border-color:
            rgba(233, 213, 255, 0.85);
    }

    .stButton > button:active {
        transform:
            translateY(0)
            scale(0.99);
    }


    /* =====================================================
       SCORE
       ===================================================== */

    .score-container {
        padding: 38px 30px;

        border-radius: 23px;

        background:
            linear-gradient(
                145deg,
                rgba(139, 92, 246, 0.13),
                rgba(30, 27, 46, 0.75)
            );

        border:
            1px solid
            rgba(168, 85, 247, 0.24);

        box-shadow:
            0 20px 65px
            rgba(0, 0, 0, 0.28);

        text-align: center;

        margin-top: 20px;
        margin-bottom: 20px;

        transition:
            transform 0.35s ease,
            box-shadow 0.35s ease,
            border-color 0.35s ease;
    }

    .score-container:hover {
        transform:
            translateY(-6px)
            scale(1.01);

        border-color:
            rgba(192, 132, 252, 0.42);

        box-shadow:
            0 25px 75px
            rgba(139, 92, 246, 0.20);
    }

    .score-label {
        color: #c4b5fd;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .score-value {
        font-size: 64px;
        font-weight: 800;
        letter-spacing: -2px;

        background:
            linear-gradient(
                90deg,
                #c4b5fd,
                #a855f7,
                #e9d5ff
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        text-shadow:
            0 0 30px
            rgba(168, 85, 247, 0.25);

        transition:
            transform 0.3s ease;
    }

    .score-container:hover .score-value {
        transform: scale(1.05);
    }

    .score-description {
        color: #aaa7b8;
        font-size: 15px;
        margin-top: 8px;
    }


    /* =====================================================
       SUMMARY CARDS
       ===================================================== */

    .summary-card {
        padding: 23px;

        min-height: 125px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(39, 39, 52, 0.92),
                rgba(27, 27, 39, 0.88)
            );

        border:
            1px solid
            rgba(168, 85, 247, 0.17);

        box-shadow:
            0 10px 32px
            rgba(0, 0, 0, 0.22);

        transition:
            transform 0.35s ease,
            box-shadow 0.35s ease,
            border-color 0.35s ease;
    }

    .summary-card:hover {
        transform:
            translateY(-8px)
            scale(1.035);

        border-color:
            rgba(192, 132, 252, 0.55);

        box-shadow:
            0 20px 50px
            rgba(139, 92, 246, 0.22);
    }

    .summary-icon {
        font-size: 25px;
        margin-bottom: 8px;
        color: #c4b5fd;
    }

    .summary-label {
        color: #aaa9b7;
        font-size: 14px;
    }

    .summary-value {
        font-size: 32px;
        font-weight: 750;
        color: #f5f3ff;
        margin-top: 4px;
    }


    /* =====================================================
       COMPACT SKILL PILLS
       ===================================================== */

    .skills-analysis {
        padding: 4px 0 8px 0;
    }

    .skill-group {
        margin-bottom: 24px;
    }

    .skill-group-title {
        font-size: 19px;
        font-weight: 650;
        margin-bottom: 12px;
        color: #f5f3ff;
    }

    .skill-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .skill-pill {
        display: inline-flex;
        align-items: center;

        padding: 9px 14px;

        border-radius: 999px;

        background:
            linear-gradient(
                145deg,
                rgba(42, 42, 56, 0.96),
                rgba(32, 32, 45, 0.96)
            );

        border:
            1px solid
            rgba(139, 92, 246, 0.24);

        color: #eeeef5;
        font-size: 14px;

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease,
            background 0.25s ease;
    }

    .skill-pill:hover {
        transform:
            translateY(-3px)
            scale(1.04);

        border-color:
            rgba(192, 132, 252, 0.65);

        background:
            linear-gradient(
                145deg,
                rgba(67, 48, 92, 0.98),
                rgba(42, 35, 58, 0.98)
            );

        box-shadow:
            0 10px 25px
            rgba(139, 92, 246, 0.20);
    }

    .skill-pill.missing {
        background:
            linear-gradient(
                145deg,
                rgba(71, 39, 55, 0.92),
                rgba(52, 32, 43, 0.92)
            );

        border-color:
            rgba(244, 114, 182, 0.22);

        color: #f8d7e8;
    }

    .skill-pill.missing:hover {
        border-color:
            rgba(244, 114, 182, 0.55);

        box-shadow:
            0 10px 25px
            rgba(236, 72, 153, 0.16);
    }


    /* =====================================================
       COMPACT RECOMMENDATION
       ===================================================== */

    .compact-recommendation {
        margin-top: 22px;
        padding: 16px 19px;

        border-radius: 15px;

        background:
            linear-gradient(
                145deg,
                rgba(76, 54, 111, 0.30),
                rgba(38, 34, 55, 0.70)
            );

        border:
            1px solid
            rgba(192, 132, 252, 0.22);

        color: #d8d5df;

        font-size: 14px;
        line-height: 1.6;

        transition:
            transform 0.3s ease,
            box-shadow 0.3s ease;
    }

    .compact-recommendation:hover {
        transform: translateY(-3px);

        box-shadow:
            0 12px 30px
            rgba(139, 92, 246, 0.14);
    }

    .compact-recommendation strong {
        color: #ddd6fe;
    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {
        border: none !important;
        height: 1px !important;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(168, 85, 247, 0.40),
                transparent
            ) !important;

        margin: 45px 0 !important;
    }


    /* =====================================================
       PROGRESS BAR
       ===================================================== */

    [data-testid="stProgress"] {
        margin-top: 10px;
        margin-bottom: 25px;
    }

    [data-testid="stProgress"] > div > div > div {
        background:
            linear-gradient(
                90deg,
                #6d28d9,
                #8b5cf6,
                #c084fc
            ) !important;
    }


    /* =====================================================
       STREAMLIT ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 18px;
            padding-right: 18px;
        }

        .main-title {
            font-size: 34px;
        }

        .brand-container {
            flex-direction: column;
            gap: 10px;
        }

        .brand-icon {
            width: 50px;
            height: 50px;
        }

        .brand-icon svg {
            width: 28px;
            height: 28px;
        }

        .score-value {
            font-size: 50px;
        }

        .skill-pill {
            font-size: 13px;
            padding: 8px 12px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.html(
    """
    <div class="hero">

        <div class="brand-container">

            <div class="brand-icon">

                <svg viewBox="0 0 24 24">

                    <circle
                        cx="12"
                        cy="12"
                        r="3.2"
                    />

                    <path d="M12 2.5v3" />
                    <path d="M12 18.5v3" />
                    <path d="M2.5 12h3" />
                    <path d="M18.5 12h3" />

                    <path d="M5.3 5.3l2.2 2.2" />
                    <path d="M16.5 16.5l2.2 2.2" />

                    <path d="M18.7 5.3l-2.2 2.2" />
                    <path d="M7.5 16.5l-2.2 -2.2" />

                </svg>

            </div>

            <div class="main-title">
                Resume Match AI
            </div>

        </div>

        <div class="subtitle">
            Analyze how closely your resume matches a job description.
        </div>

    </div>
    """
)


# =========================================================
# UPLOAD RESUME
# =========================================================

st.html(
    """
    <div class="section-title scroll-reveal">
        <span class="section-number">1</span>
        Upload Your Resume
    </div>
    """
)

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"],
    help="Upload your resume in PDF or Word (.docx) format."
)


# =========================================================
# JOB DESCRIPTION
# =========================================================

st.html(
    """
    <div class="section-title scroll-reveal">
        <span class="section-number">2</span>
        Enter Job Description
    </div>
    """
)

job_text = st.text_area(
    "Paste the job description below",
    height=220,
    placeholder=(
        "Example:\n\n"
        "We are looking for a Python Developer with experience "
        "in Python, SQL, Git, JavaScript, AWS and Docker."
    )
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

analyze = st.button(
    "✦  Analyze Resume",
    use_container_width=True
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if uploaded_file is None:

        st.warning(
            "Please upload your resume in PDF or Word (.docx) format."
        )

    elif not job_text.strip():

        st.warning(
            "Please enter a job description."
        )

    else:

        temp_resume_path = None

        try:

            # =================================================
            # SAVE UPLOADED FILE
            # =================================================

            file_extension = os.path.splitext(
                uploaded_file.name
            )[1].lower()

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_resume_path = temp_file.name


            # =================================================
            # EXTRACT RESUME TEXT
            # =================================================

            if file_extension == ".pdf":

                resume_text = extract_text_from_pdf(
                    temp_resume_path
                )

            elif file_extension == ".docx":

                resume_text = extract_text_from_docx(
                    temp_resume_path
                )

            else:

                st.error(
                    "Unsupported file format."
                )

                st.stop()


            # =================================================
            # CHECK EXTRACTED TEXT
            # =================================================

            if not resume_text.strip():

                st.warning(
                    "No readable text was found in the uploaded resume."
                )

                st.stop()


            # =================================================
            # EXTRACT SKILLS
            # =================================================

            resume_skills = extract_skills(
                resume_text
            )

            job_skills = extract_skills(
                job_text
            )


            # =================================================
            # COMPARE SKILLS
            # =================================================

            (
                matching_skills,
                missing_skills,
                match_percentage
            ) = compare_skills(
                resume_skills,
                job_skills
            )


            # =================================================
            # RESULTS HEADER
            # =================================================

            st.divider()

            st.html(
                """
                <div class="section-title scroll-reveal">
                    ✦ Resume Analysis
                </div>
                """
            )


            # =================================================
            # SCORE
            # =================================================

            st.html(
                f"""
                <div class="score-container scroll-reveal">

                    <div class="score-label">
                        Skill Match Score
                    </div>

                    <div class="score-value">
                        {match_percentage:.2f}%
                    </div>

                    <div class="score-description">
                        {len(matching_skills)}
                        of
                        {len(job_skills)}
                        required skills matched
                    </div>

                </div>
                """
            )

            st.progress(
                min(int(match_percentage), 100)
            )


            # =================================================
            # SUMMARY CARDS
            # =================================================

            st.html(
                """
                <div style="height:8px;"></div>
                """
            )

            col1, col2, col3 = st.columns(3)


            with col1:

                st.html(
                    f"""
                    <div class="summary-card scroll-reveal">

                        <div class="summary-icon">
                            ✓
                        </div>

                        <div class="summary-label">
                            Matching Skills
                        </div>

                        <div class="summary-value">
                            {len(matching_skills)}
                        </div>

                    </div>
                    """
                )


            with col2:

                st.html(
                    f"""
                    <div class="summary-card scroll-reveal">

                        <div class="summary-icon">
                            !
                        </div>

                        <div class="summary-label">
                            Missing Skills
                        </div>

                        <div class="summary-value">
                            {len(missing_skills)}
                        </div>

                    </div>
                    """
                )


            with col3:

                st.html(
                    f"""
                    <div class="summary-card scroll-reveal">

                        <div class="summary-icon">
                            ◈
                        </div>

                        <div class="summary-label">
                            Resume Skills
                        </div>

                        <div class="summary-value">
                            {len(resume_skills)}
                        </div>

                    </div>
                    """
                )


            st.divider()


            # =================================================
            # COMPACT SKILLS ANALYSIS
            # =================================================

            st.html(
                """
                <div class="skills-analysis scroll-reveal">

                    <div class="skill-group">

                        <div class="skill-group-title">
                            ✓ Matching Skills
                        </div>

                    </div>

                </div>
                """
            )


            if matching_skills:

                matching_pills = "".join(
                    f"""
                    <div class="skill-pill">
                        ✓ &nbsp; {skill.title()}
                    </div>
                    """
                    for skill in matching_skills
                )

                st.html(
                    f"""
                    <div class="skill-pills scroll-reveal">
                        {matching_pills}
                    </div>
                    """
                )

            else:

                st.info(
                    "No matching skills found."
                )


            st.html(
                """
                <div style="height:18px;"></div>

                <div class="skill-group-title scroll-reveal">
                    × Missing Skills
                </div>
                """
            )


            if missing_skills:

                missing_pills = "".join(
                    f"""
                    <div class="skill-pill missing">
                        × &nbsp; {skill.title()}
                    </div>
                    """
                    for skill in missing_skills
                )

                st.html(
                    f"""
                    <div class="skill-pills scroll-reveal">
                        {missing_pills}
                    </div>
                    """
                )

            else:

                st.success(
                    "No missing skills!"
                )


            # =================================================
            # COMPACT RECOMMENDATION
            # =================================================

            if missing_skills:

                missing_text = ", ".join(
                    skill.title()
                    for skill in missing_skills
                )

                st.html(
                    f"""
                    <div class="compact-recommendation scroll-reveal">

                        💡 <strong>Suggestion:</strong>
                        If you have relevant experience with
                        {missing_text}, consider highlighting
                        it in your resume.

                    </div>
                    """
                )

            else:

                st.success(
                    "Your resume contains all recognized skills "
                    "required by this job description."
                )


        except Exception as error:

            st.error(
                f"Something went wrong while analyzing the resume: {error}"
            )


        finally:

            # =================================================
            # DELETE TEMPORARY FILE
            # =================================================

            if (
                temp_resume_path
                and os.path.exists(temp_resume_path)
            ):

                try:

                    os.remove(temp_resume_path)

                except OSError:

                    pass