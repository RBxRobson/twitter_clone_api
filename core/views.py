from django.shortcuts import render
import markdown


def read_readme(request):
    # Abrir o arquivo README.md
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    # Converter Markdown para HTML
    html_content = markdown.markdown(readme_content)

    # Retornar o conteúdo HTML renderizado no template
    return render(request, "home.html", {"content": html_content})
