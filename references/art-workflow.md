# Sample-First Art, Animation and Audio

## Prototype to First Art Pass

Start from the playable HTML/white-box build and accepted gameplay, not a new marketing layout. Capture actual screens and map each visible placeholder to a scene node, asset ID and interaction state. Preserve layout constraints, readable information and hit areas while replacing presentation.

Co-design an art direction sheet: visual reference, camera/perspective, palette, line/texture treatment, light direction, target dimensions, safe areas and forbidden variations. HTML is a layout/behavior reference; do not imply automatic HTML-to-Godot scene conversion.

Integrate representative character, background and UI samples as needed to expose the highest-risk combination. Inspect in-engine scale, contrast, alpha edges, layering, readable text, input states and desktop/mobile framing where relevant. Get sample acceptance before expanding the batch.

## Batch Contract

Maintain an editable asset manifest, normally CSV/JSON/XLSX. Minimum shared fields:

`asset_id, category, source_path, runtime_path, width, height, format, alpha, anchor, layer, style_revision, prompt_revision, status`

Add category-specific fields only when relevant:

- Characters: identity reference, silhouette, costume, pose/expression/state, feet/pivot anchor; separate characters from furniture/props when independently animated or layered.
- Backgrounds: camera angle, horizon, foreground/midground separation, safe UI area and tile edges when applicable.
- UI: normal/hover/pressed/disabled/selected states, nine-slice margins and contrast. Keep dynamic/localized text in engine UI rather than baking it into images.
- Animation: state names, frame count, FPS/duration, loop mode, pivot consistency, transitions and static fallback. Choose spritesheets, separate frames or engine tweens based on the game.
- Audio: event ID, duration, loop points, gain/bus, variation, interruption/concurrency and mute behavior.

Use a shared prompt formula:

```text
Approved style/identity anchor + category contract + this asset's variable content
+ camera/light/composition + dimensions/alpha/layers + exclusions
```

Store shared specifications once; each manifest row supplies variation. Freeze style/prompt revision after sample approval. Produce a small inspection batch before the full set if variation risk remains. Verify provider/tool availability, credentials, cost and license terms before generation; Higgsfield is optional, not required.

## Integration and Revision

Keep originals and engine-ready derivatives separately. Preserve actual slicing/atlas/import scripts with explicit input/output arguments, dependencies and run examples. Do not copy project-specific hardcoded scripts into this skill without adapting and testing them.

Integrate assets in manifest order, set import/filter/alpha options, wire animation states and verify interactions. Check screenshots and an actual playthrough, not just file existence. For rejection, record affected IDs, reason and desired revision; regenerate only those assets while preserving accepted references. A style-wide change needs a new shared revision and scope decision.

Finish with the accepted manifest, source/runtime mapping, reusable commands, visual evidence and limitations. The skill ships the production protocol, not a universal image generator or atlas pipeline; create those helpers only for a selected toolchain.
