
# ── Research Fields (comprehensive) ──────────────────────────────────────────
RESEARCH_FIELDS = [
    # Physical Sciences
    "Physics", "Quantum Physics", "Astrophysics & Cosmology", "Particle Physics",
    "Nuclear Physics", "Condensed Matter Physics", "Optics & Photonics",
    # Chemistry
    "Chemistry", "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry",
    "Biochemistry", "Analytical Chemistry", "Materials Chemistry",
    # Biology & Life Sciences
    "Biology", "Molecular Biology", "Cell Biology", "Genetics & Genomics",
    "Microbiology", "Ecology", "Evolutionary Biology", "Neuroscience", "Physiology",
    "Botany", "Zoology", "Marine Biology",
    # Medicine & Health
    "Medicine", "Clinical Research", "Public Health", "Pharmacology", "Oncology",
    "Neurology", "Cardiology", "Immunology", "Psychiatry", "Epidemiology",
    "Biomedical Research", "Surgery", "Dental Science", "Veterinary Science",
    # Computer Science & Technology
    "Computer Science", "Artificial Intelligence", "Machine Learning", "Data Science",
    "Cybersecurity", "Software Engineering", "Human-Computer Interaction",
    "Computer Vision", "Natural Language Processing", "Robotics",
    "Quantum Computing", "Distributed Systems", "Blockchain",
    # Mathematics
    "Mathematics", "Pure Mathematics", "Applied Mathematics", "Statistics",
    "Number Theory", "Topology", "Computational Mathematics", "Probability Theory",
    # Engineering
    "Electrical Engineering", "Mechanical Engineering", "Civil Engineering",
    "Chemical Engineering", "Biomedical Engineering", "Aerospace Engineering",
    "Environmental Engineering", "Materials Science & Engineering",
    "Industrial Engineering", "Petroleum Engineering",
    # Social Sciences & Humanities
    "Psychology", "Sociology", "Economics", "Political Science",
    "Anthropology", "History", "Philosophy", "Education Research",
    "Law & Legal Studies", "Linguistics", "Cultural Studies", "Archaeology",
    # Environmental & Earth Sciences
    "Environmental Science", "Climate Science", "Earth Science", "Oceanography",
    "Atmospheric Science", "Geology", "Geography", "Hydrology",
    # Business & Management
    "Business Administration", "Finance", "Marketing", "Management Science",
    "Entrepreneurship", "Supply Chain Management", "Organizational Behavior",
    # Interdisciplinary
    "Cognitive Science", "Bioinformatics", "Systems Biology", "Nanotechnology",
    "Biotechnology", "Neurotechnology", "Science Policy", "Ethics in Research",
    "Urban Studies", "Energy Studies", "Food Science & Nutrition",
    "Other",
]

def global_constants(request):
    return {
        'RESEARCH_FIELDS': RESEARCH_FIELDS,
        'app_name': 'PeerMatch',
    }
