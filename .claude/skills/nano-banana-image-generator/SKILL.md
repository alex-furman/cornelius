---
name: nano-banana-image-generator
description: Generate images using Google's Nano Banana (Gemini 2.5 Flash Image). Use when creating infographics, diagrams, thumbnails, social media graphics, or any AI-generated images. Costs $0.039/image.
allowed-tools: Bash, Read, Write
---

# Nano Banana Image Generator

Generate images using Google's Gemini 2.5 Flash Image model (codename: Nano Banana).

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Generate Script | `.claude/skills/nano-banana-image-generator/scripts/generate.sh` | ✓ | | Shell helper |
| Thumbnail Script | `.claude/skills/nano-banana-image-generator/scripts/generate_thumbnail.py` | ✓ | | 16:9 thumbnail generator |
| Image Script | `.claude/skills/nano-banana-image-generator/scripts/generate_image.py` | ✓ | | Python with aspect ratio control |
| Best Practices | `.claude/skills/nano-banana-image-generator/best_practices.md` | ✓ | | Prompt engineering guidelines |
| API Key | `$GOOGLE_API_KEY` or `$GEMINI_API_KEY` | ✓ | | Required for API access |
| Output Directory | `$OUTPUT_DIR` or current directory | | ✓ | Where images are saved |
| Generated Image | User-specified path | | ✓ | Output PNG file |

## Quick Start

Run from the repository root with Python and `requests` already installed.
Use the bundled Python generator for prompts containing quotes; it serializes
JSON correctly. A separate `~/.claude/skills` installation is not required.
Set `image_prompt`, `image_output` and `image_ratio` to the requested prompt,
output-file path and aspect ratio, respectively, using quoted data rather than
interpolating user text into shell code. Then run:

```bash
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" "$image_prompt" "$image_output" --aspect-ratio "$image_ratio"
```

**Generate a 16:9 thumbnail:**
```bash
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" "YouTube thumbnail showing AI agents" "/tmp/thumb.png" --aspect-ratio "16:9"
```

**Generate with custom output directory:**
```bash
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" "Sunset over mountains" "/tmp/output images/sunset.png"
```

Report missing dependencies or credentials without claiming generation. After
each call, inspect the actual output image before reporting success; a zero exit
status alone is insufficient (the legacy thumbnail helper can exit zero after
an API failure). In Codex, use the exposed native image viewer; Claude Code uses
Read on the image. If viewing is unavailable, report that visual verification
is incomplete. Never substitute another image provider silently.

## Scripts

| Script | Purpose | Output |
|--------|---------|--------|
| `scripts/generate.sh` | General image generation | 1024x1024 PNG |
| `scripts/generate_thumbnail.py` | 16:9 thumbnails | 1344x768 PNG |
| `scripts/generate_image.py` | Python with aspect ratio control | Configurable |

## Pricing & Limits

- **Cost**: $0.039 per image
- **Free tier**: 500 requests/day
- **Generation time**: ~22 seconds
- **Resolution**: 1024x1024 (square), 1344x768 (16:9)

## Best Practices

For detailed prompt engineering and brand styling guidelines, see [best_practices.md](best_practices.md).

### Critical Constraints

| Element | Maximum |
|---------|---------|
| Visual boxes/shapes | **10 maximum** |
| Text pieces/labels | **10 maximum** |
| Hierarchy levels | **3 maximum** |

### Prompt Structure

**DO:** Write narrative descriptions
```
Create a simple infographic with black background showing a central concept
with 4-5 supporting elements. Use white text, DM Sans font, bold titles.
```

**DON'T:** Use keyword lists
```
LinkedIn post, gradient, red, white, large text, 15 boxes, arrows everywhere
```

### Brand Styling (the user's)

Include in prompts for brand consistency:
```
Use the user's brand style: black background (#000000), white text (#ffffff),
DM Sans font, bold 700 weight for titles, clean minimal design.
```

## Use Cases

**Perfect For:**
- Social media infographics and carousels
- YouTube thumbnails
- Diagrams and technical documentation
- Product mockups
- Mobile-optimized content

**Not Ideal For:**
- Hyper-realistic photography
- Complex multi-font typography
- Fine detail technical renders

## Environment Variables

- `GOOGLE_API_KEY` or `GEMINI_API_KEY` - API key (required)
- `OUTPUT_DIR` - Shell helper only; Python scripts take the output path as an argument

## Examples

**Infographic:**
```bash
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" "Simple framework diagram with black background. CENTER: 'AI Agents' in large white text. SURROUNDING: 4 icons for Planning, Memory, Tools, Learning. DM Sans font, minimal design." "agents_framework.png"
```

**Thumbnail:**
```bash
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" "Professional YouTube thumbnail: bold white text 'DEEP AGENTS' on dramatic black background with subtle blue glow, tech aesthetic" "deep_agents_thumb.png" --aspect-ratio "16:9"
```

## Completion Checklist

- [ ] API key verified (GOOGLE_API_KEY or GEMINI_API_KEY)
- [ ] Prompt crafted following best practices (narrative description, not keyword lists)
- [ ] Critical constraints respected (max 10 boxes, max 10 text pieces, max 3 hierarchy levels)
- [ ] Appropriate script selected (generate.sh, generate_thumbnail.py, or generate_image.py)
- [ ] Output directory confirmed or created
- [ ] Image generated successfully (~22 seconds)
- [ ] Output file path provided to user
- [ ] Cost noted ($0.039 per image)
