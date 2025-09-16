#version 300 es
precision highp float;

uniform float uTime;
in vec2 vUv;
out vec4 fragColor;

void main() {
    vec2 uv = vUv * 2.0 - 1.0;

    float angle = atan(uv.y, uv.x);
    float radius = length(uv);

    // закручиваем угол по времени
    angle += uTime * 0.5;
    float waves = sin(angle * 5.0 + radius * 20.0 - uTime * 2.0);

    vec3 color = vec3(
        0.5 + 0.5 * sin(waves + uTime),
        0.5 + 0.5 * cos(waves + uTime * 0.7),
        0.5 + 0.5 * sin(radius * 10.0 - uTime)
    );

    fragColor = vec4(color * (1.0 - radius), 1.0);
}

