#version 300 es
precision highp float;

uniform float uTime;
in vec2 vUv;
out vec4 fragColor;

void main() {
    vec2 uv = vUv * 10.0; // увеличиваем сетку
    uv += uTime * 0.5;    // сдвигаем её во времени

    // «решётка» через frac (дробную часть)
    vec2 grid = fract(uv);

    float line = step(grid.x, 0.05) + step(grid.y, 0.05);

    vec3 color = mix(
        vec3(0.0, 0.0, 0.0),
        vec3(0.2 + 0.8 * sin(uTime), 0.3, 1.0),
        line
    );

    fragColor = vec4(color, 1.0);
}

