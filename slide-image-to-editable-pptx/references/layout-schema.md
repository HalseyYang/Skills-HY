# Editable Slide Layout JSON

The helper script accepts JSON with this shape:

```json
{
  "slide_size": "wide",
  "slides": [
    {
      "background": "#FFFFFF",
      "elements": [
        {
          "type": "text",
          "text": "Slide title",
          "x": 0.08,
          "y": 0.06,
          "w": 0.84,
          "h": 0.12,
          "font_size": 32,
          "bold": true,
          "color": "#111827",
          "align": "left"
        },
        {
          "type": "rect",
          "x": 0.08,
          "y": 0.22,
          "w": 0.34,
          "h": 0.18,
          "fill": "#EAF6F2",
          "line": "#1F7A6D"
        },
        {
          "type": "table",
          "x": 0.08,
          "y": 0.45,
          "w": 0.84,
          "h": 0.36,
          "rows": [
            ["Metric", "Value"],
            ["Accuracy", "95%"]
          ],
          "font_size": 12
        },
        {
          "type": "image",
          "path": "/absolute/path/to/cropped-chart.png",
          "x": 0.55,
          "y": 0.22,
          "w": 0.35,
          "h": 0.20
        }
      ]
    }
  ]
}
```

## Element Types

### `text`

Editable text box.

Fields:

- `text`: string
- `x`, `y`, `w`, `h`: normalized coordinates
- `font_size`: points
- `font_face`: optional, default Arial
- `bold`, `italic`: booleans
- `color`: hex color
- `align`: `left`, `center`, or `right`
- `fill`: optional text box fill color
- `line`: optional border color

### `rect`

Editable rectangle.

Fields:

- `x`, `y`, `w`, `h`
- `fill`: hex color or `transparent`
- `line`: hex color or `transparent`
- `radius`: optional, currently advisory only

### `line`

Editable line.

Fields:

- `x`, `y`, `w`, `h`: line start and extent
- `line`: hex color
- `width`: line width in points

### `table`

Editable PowerPoint table.

Fields:

- `rows`: two-dimensional array of strings
- `x`, `y`, `w`, `h`
- `font_size`
- `header_fill`, `body_fill`, `text_color`: optional hex colors

### `image`

Embedded image for complex content that should not be recreated manually.

Fields:

- `path`: absolute or layout-file-relative image path
- `x`, `y`, `w`, `h`

## Reconstruction Notes

Use normalized coordinates and keep a companion note for uncertain items:

```json
{
  "notes": [
    "Slide 3 chart values are approximate because source image labels are blurred.",
    "Slide 5 product screenshot retained as image."
  ]
}
```
