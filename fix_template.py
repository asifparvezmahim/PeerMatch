import os

template = r"""{% extends "layout.html" %}
{% load static %}

{% block content %}
<div style="display: flex; justify-content: center; min-height: 80vh; padding: 2rem 0;">
    <div class="glass" style="padding: 3rem; width: 100%; max-width: 750px; align-self: flex-start;">
        <h2 style="margin-bottom: 0.5rem; font-size: 1.8rem;">{{ action }} Research Idea</h2>
        <p style="color: var(--text-muted); margin-bottom: 2rem;">Fill in the details to attract the right collaborators.</p>
        <form method="POST">
            {% csrf_token %}
            <h4 style="color: var(--primary-color); margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--glass-border);">
                Basic Information</h4>
            <div class="form-group">
                <label>Title of the Idea</label>
                <input type="text" name="title" required value="{{ idea.title|default:'' }}"
                    placeholder="A compelling research direction...">
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div class="form-group">
                    <label>Research Field</label>
                    <select name="field">
                        {% for f in RESEARCH_FIELDS %}
                        <option value="{{ f }}" {% if idea and idea.field == f %}selected{% endif %}>{{ f }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label>Keywords (comma separated)</label>
                    <input type="text" name="keywords" value="{{ idea.keywords|default:'' }}"
                        placeholder="AI, Genomics, Climate...">
                </div>
            </div>
            <div class="form-group">
                <label>Abstract / Description</label>
                <textarea name="description" rows="4" required
                    placeholder="Describe your research idea in detail...">{{ idea.description|default:'' }}</textarea>
            </div>
            <h4 style="color: var(--success); margin: 1.5rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--glass-border);">
                Collaboration Details</h4>
            <div class="form-group">
                <label>Work Done So Far</label>
                <textarea name="progress" rows="3"
                    placeholder="What has already been completed, prototyped, or researched?">{{ idea.progress|default:'' }}</textarea>
            </div>
            <div class="form-group">
                <label>Where Help is Needed</label>
                <textarea name="help_needed" rows="3"
                    placeholder="Exactly what you need help with and at what stage of the research...">{{ idea.help_needed|default:'' }}</textarea>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div class="form-group">
                    <label>Skills Needed (comma separated)</label>
                    <input type="text" name="skills_needed" value="{{ idea.skills_needed|default:'' }}"
                        placeholder="Python, Data Analysis, Lab Work...">
                </div>
                <div class="form-group">
                    <label>Expertise Needed (comma separated)</label>
                    <input type="text" name="expertise_needed" value="{{ idea.expertise_needed|default:'' }}"
                        placeholder="Machine Learning, Biochemistry...">
                </div>
            </div>
            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1.5rem; padding: 1rem;">
                {{ action }} Idea
            </button>
        </form>
    </div>
</div>
{% endblock %}
"""

target = r"e:\My Django Project\Research Partner\research_platform\peermatch\core\templates\idea_form.html"

with open(target, 'w', encoding='utf-8') as f:
    f.write(template)

# Verify
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

if 'idea.field == f' in content and 'idea.field==f' not in content:
    print("SUCCESS: File written correctly - spaces present around ==")
else:
    print("FAILED - still contains bad syntax:")
    for i, line in enumerate(content.splitlines(), 1):
        if '==f' in line:
            print(f"  Line {i}: {line}")
