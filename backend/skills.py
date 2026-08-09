def extract_skills(text):

    text = text.lower()

    skills = [
        "python",
        "c",
        "c++",
        "java",
        "javascript",
        "html",
        "css",
        "sql",
        "react",
        "node",
        "fastapi",
        "flask",
        "django",
        "git",
        "github",
        "docker",
        "linux",
        "numpy",
        "pandas",
        "tensorflow",
        "pytorch",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "excel",
        "powerpoint",
        "word",
        "opencv",
        "raspberry pi",
        "arduino",
        "esp32"
    ]

    found = []

    for skill in skills:
        if skill in text:
            found.append(skill.title())

    return sorted(list(set(found)))