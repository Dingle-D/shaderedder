#version 300 es
precision highp float;

uniform float uTime;
in vec2 vUv;
out vec4 fragColor;

// простая функция псевдослучайности
float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

void main() {
    vec2 uv = vUv * 50.0; // много звёзд

    vec2 cell = floor(uv);
    vec2 f = fract(uv);

    float star = step(0.995, hash(cell)); // редкие точки
    float twinkle = sin(uTime * 5.0 + hash(cell) * 10.0) * 0.5 + 0.5;

    vec3 color = vec3(star * twinkle);

    fragColor = vec4(color, 1.0);
}

