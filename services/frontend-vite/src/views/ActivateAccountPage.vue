<template>
    <div class="activation-container">
      <h1 v-if="error">{{ error }}</h1>
      <h1 v-else-if="success"> Account successfuly activated!</h1>
      <h1 v-else>Activating account...</h1>
  
      <router-link 
        to="home" 
        class="auth-link"
      >
        Home
      </router-link>
    </div>
</template>

<script>
import { mapState, mapActions, mapMutations } from "vuex";

export default {
  data() {
    return {
      success: false
    }
  },
  async created() {
    const token = this.$route.query.token
    if (!token) {
      this.SET_ERROR('Token is missing');
      return;
    }

    this.activateAccount(token);
    this.success = true; // FIX: Backend должен выкинуть статус-код ошибку при повторении токена, а не вернуть success: false
  },
  methods: {
    ...mapActions('auth', ['CONFIRM']),
    ...mapMutations('auth', ['SET_ERROR']),

    activateAccount(token) {
      this.$store
        .dispatch(
          'CONFIRM',
          token
        )
        .catch((error) => console.log("Error in onSubmit:", error));
    }
  },
  computed: {
    ...mapState({
      error: state => state.auth.errors
    })
  }
}
</script>

<style scoped>
.activation-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  text-align: center;
}

.auth-link {
  display: inline-block;
  margin-top: 1rem;
  color: #42b983;
}
</style>
