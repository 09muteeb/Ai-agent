def get_career_roadmap(career_name):
    roadmaps = {
        "software engineer": ["Learn Python/Java", "Understand Data Structures", "Build Projects", "Use Git/GitHub", "Apply for Internships"],
        "graphic designer": ["Master Photoshop/Illustrator", "Learn Color Theory", "Understand Typography", "Build Portfolio", "Freelance Projects"],
        "data analyst": ["Learn Excel & SQL", "Use Python or R", "Learn Data Visualization", "Understand Statistics", "Build Dashboards"],
        "doctor": ["Earn Medical Degree", "Pass Licensing Exams", "Complete Residency", "Choose Specialization", "Start Practice"],
        "teacher": ["Get Education Degree", "Develop Lesson Planning Skills", "Understand Child Psychology", "Pass Certification", "Start Teaching"],
        "civil engineer": ["Earn Engineering Degree", "Learn AutoCAD", "Study Structures & Materials", "Get Site Experience", "Get PE License"],
        "mechanical engineer": ["Learn Mechanics & Thermodynamics", "CAD Tools", "Internships", "SolidWorks/ANSYS", "Get Certified"],
        "accountant": ["Study Accounting Principles", "Learn Excel & QuickBooks", "Get Certified (ACCA/CPA)", "Practice Tax Filing", "Internships"],
        "lawyer": ["Earn Law Degree", "Pass Bar Exam", "Learn Legal Research", "Intern at Firms", "Practice in Court"],
        "psychologist": ["Study Psychology", "Get Masters or PhD", "Intern at Clinics", "Learn Counseling Techniques", "License Exam"],
        "nurse": ["Get Nursing Degree", "Pass NCLEX", "Clinical Rotations", "Specialize (ICU, ER)", "Join a Hospital"],
        "digital marketer": ["Learn SEO/SEM", "Understand Social Media", "Email Marketing", "Google Analytics", "Run Ad Campaigns"],
        "entrepreneur": ["Understand Business Models", "Build MVP", "Marketing Strategies", "Pitch to Investors", "Manage Finances"],
        "chef": ["Culinary School", "Knife Skills", "Understand Cuisines", "Kitchen Internships", "Open Restaurant"],
        "pilot": ["Get Flying License", "Flight School", "Learn Navigation & Instruments", "Log Flying Hours", "Join Airline"]
    }

    return roadmaps.get(career_name.lower(), ["Sorry, no roadmap found."])
