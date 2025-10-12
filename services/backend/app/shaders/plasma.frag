#version 300 es
precision highp float;

uniform float uTime;
in vec2 vUv;
out vec4 fragColor;

void main() {
    vec2 uv = vUv * 5.0;

    float pattern =
          sin(uv.x + uTime)
        + sin(uv.y + uTime)
        + sin(uv.x + uv.y + uTime)
        + sin(length(uv) + uTime);

    float val = pattern * 0.25;

    vec3 color = vec3(
        0.5 + 0.5 * sin(val * 3.0 + uTime),
        0.5 + 0.5 * cos(val * 5.0 + uTime),
        0.5 + 0.5 * sin(val * 7.0 - uTime)
    );

    fragColor = vec4(color, 1.0);
}

