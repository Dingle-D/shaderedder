#version 300 es
precision highp float;
precision highp int;

uniform float     uTime;                 // shader playback time (in seconds)
uniform float     uTimeDelta;            // render time (in seconds)
uniform vec3      uResolution;           // viewport resolution (in pixels)
out vec4 fragColor;

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = fragCoord/uResolution.xy;

    // Time varying pixel color
    vec3 col = 0.5 + 0.5*cos(uTime1+uv.xyx+vec3(0,2,4));

    // Output to screen
    fragColor = vec4(col,1.0);
}

void main() {
    mainImage(fragColor, gl_FragCoord.xy);
}

