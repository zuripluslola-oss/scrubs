# Photos for Must Love Scrubs

Drop real photo files here and rebuild — they get embedded into the site and
the clickable bundle automatically. Until a file exists, its slot shows a
tasteful gradient so nothing looks broken.

## Filenames the site looks for

| Filename              | Where it appears                                             |
|-----------------------|-------------------------------------------------------------|
| `nurses-group.jpg`    | Homepage "for nurses, by nurses" intro + Study Guide intro   |
| `dictionary.jpg`      | Nurse Dictionary product art (homepage teaser + dict page)   |

Use `.jpg` (or change the reference in `tools/build_pages.py`). Landscape,
at least ~1200px wide, looks best. After adding a file:

```
python3 tools/build_pages.py && python3 tools/bundle_site.py
```
