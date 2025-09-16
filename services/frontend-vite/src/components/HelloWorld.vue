// ThreeScene.vue
<template>
  <div ref="container" style="w-full h-full"></div>
</template>

<script>
import * as THREE from 'three';

export default {
  name: 'ThreeScene',
  data() {
    return {
      renderer: null,
      scene: null,
      camera: null,
      cube: null
    };
  },
  mounted() {
    this.initScene();
    this.renderScene();
  },
  beforeDestroy() {
    this.renderer.dispose();
    this.scene.dispose();
  },
  methods: {
    initScene() {
      // Create a scene
      this.scene = new THREE.Scene();

      // Create a camera
      this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
      this.camera.position.z = 5;

      // Create a renderer
      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
      this.$refs.container.appendChild(this.renderer.domElement);

      // Add a cube to the scene
      const geometry = new THREE.BoxGeometry();
      const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
      this.cube = new THREE.Mesh(geometry, material);
      this.scene.add(this.cube);
    },
    renderScene() {
      const animate = () => {
        requestAnimationFrame(animate);
        this.cube.rotation.x += 0.01;
        this.cube.rotation.y += 0.01;
        this.renderer.render(this.scene, this.camera);
      };
      animate();
    }
  }
};
</script>

<style scoped>
#container {
  width: 100%;
  height: 100%;
}
</style>

