#version 300 es
precision highp float;

uniform float uTime;
in vec2 vUv;
out vec4 fragColor;

void main() {
    vec2 uv = vUv * 2.0 - 1.0;
    float len = length(uv);

    float wave = sin(len * 20.0 - uTime * 3.0);

    vec3 color = vec3(
        0.5 + 0.5 * sin(uTime + wave),
        0.5 + 0.5 * sin(uTime + wave + 2.0),
        0.5 + 0.5 * sin(uTime + wave + 4.0)
    );

    fragColor = vec4(color, 1.0);
}

