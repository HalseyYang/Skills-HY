---
name: ppt-generator-pro
description: Generate high-quality AI-assisted PPT slide images and presentation videos from documents or text using the NanoBanana PPT workflow, Gemini/Nano Banana image generation, optional Kling AI transitions, style templates, interactive HTML viewers, and FFmpeg video composition. Use when the user asks to create a PPT, presentation deck, slide images, visual presentation, AI-generated slides, animated PPT transitions, looping title animation, or export a PPT-style video from source content.
---

# PPT Generator Pro

Use this skill to create image-first PPT presentations and optional transition videos from a document, outline, or pasted text.

## Quick Start

1. Read the user's source content from a file path or pasted text.
2. Before choosing style or layout, ask the user whether to output using the company PPT template when the request is to create a PPT/deck:
   - Template asset: `assets/company-template/company-ppt-template.ppt`
   - Original source: `/Users/hanyueyang/Desktop/公司PPT template.ppt`
   - If the user says yes, preserve the company's visual identity, layout conventions, typography, colors, footer/header patterns, and page hierarchy as much as the generation workflow allows.
   - Also mention the reusable template library if the user wants a non-company PPT style:
     - `assets/template-library/business-blue-green-yellow-minimal.pptx`
     - `assets/template-library/red-navy-visual-tables.pptx`
3. Choose a style from `styles/` or `assets/template-library/` if the company template is not requested or if extra image-style guidance is needed:
   - `gradient-glass.md`: technology/business, gradient glass cards.
   - `vector-illustration.md`: warmer educational or explanatory visuals.
4. Decide page count, language, and whether video transitions are needed.
5. Ensure required environment variables are present:
   - `GEMINI_API_KEY` for slide image generation.
   - `KLING_ACCESS_KEY` and `KLING_SECRET_KEY` only for Kling video features.
6. Run the appropriate script from this skill directory:
   - `generate_ppt.py` for slide images and interactive viewer.
   - `generate_ppt_video.py` for slides plus transition videos.

Read `references/upstream-skill.md` for the full upstream workflow and parameter details.

## Workflow

1. Analyze the content.
   - Extract core message, target audience, structure, and visual story.
   - Convert long documents into a page-by-page outline before generating images.

2. Generate slide prompts.
   - Keep each slide focused on one message.
   - Use style files in `styles/` to keep visual consistency.
   - For dense professional content, favor structured cards, diagrams, timelines, matrices, and clear hierarchy.

3. Generate assets.
   - Use the repository scripts rather than rewriting the full generation pipeline.
   - Keep outputs in a project-specific folder.
   - Preserve generated prompts and image/video metadata for later editing.

4. Review quality.
   - Check that slide text is readable, not hallucinated, and matches source content.
   - Check 16:9 framing, consistent style, page order, and visual continuity.
   - For video output, verify transitions, resolution, frame rate, and audio/video duration if applicable.

## Important Files

- `assets/company-template/company-ppt-template.ppt`: company PPT template. Ask whether to use it before making PPTs.
- `assets/template-library/README.md`: reusable PPT template index.
- `assets/template-library/business-blue-green-yellow-minimal.pptx`: blue/green/yellow senior business template.
- `assets/template-library/red-navy-visual-tables.pptx`: red + dark navy visual table template.
- `generate_ppt.py`: main slide image generation flow.
- `generate_ppt_video.py`: slide plus transition-video flow.
- `kling_api.py`: Kling AI API helper.
- `transition_prompt_generator.py`: transition prompt generation.
- `video_composer.py`: video composition helper.
- `templates/viewer.html`: interactive slide viewer.
- `templates/video_viewer.html`: interactive video/image viewer.
- `styles/`: visual style prompts.
- `prompts/transition_template.md`: transition prompt template.

## Quality Rules

- Do not invent technical facts, citations, regulatory claims, or clinical claims when turning source documents into slides.
- For client or regulated content, preserve the user's meaning and mark any uncertain interpretation.
- Keep slide text concise; move dense detail into speaker notes or an appendix if needed.
- Verify generated files exist before reporting completion.
- If API keys or FFmpeg are missing, explain the missing prerequisite and provide the next command or configuration needed.

## References

- `references/upstream-skill.md`: original upstream skill instructions from `op7418/NanoBanana-PPT-Skills`.
- `references/desktop-style-pack/`: Imported desktop PPT style references with additional visual templates, color schemes, and Chinese style guides. Use when the user asks for a specific aesthetic or wants more style choices.
