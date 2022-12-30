# Potter Parser
Project that is intended to parse a vtt subtitle file for moments when Andy Potter says "this", then looks when he pointing at the part of his solar/electrical setup that he's referring to with opencv, and spits out images. This is so we can figure out part he's talking about quickly. No it's not that practical, but it's fun.

## Building
```
podman build -t potter-parser:latest .
```

## Running
```
podman run --rm -it -v /scratch/klaus/whisper_nonsense/MOV/potter_rant:/data --name=potter localhost/potter-parser:latest
```
