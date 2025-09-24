<template>
  <div>
    
  </div>
</template>

<script>
import ApiService from "@/common/api.service";
import { mapState, mapActions } from "vuex";

export default {
  name: "AppLogin",
  mounted() {
    const token = this.getCookie("access_token");
    const toktype = this.getCookie("token_type");
    
    this.onAuthorize(token, toktype)
  },
  methods: {
    ...mapActions('auth', ['LOGIN_FORCE']),

    onAuthorize(token, type) {
      this.$store
        .dispatch('LOGIN_FORCE', {
          access_token: token,
          token_type: type
        })
        .then(() => this.$router.push({name: "explore"}))
        .catch((error) => console.log("Error while autorization"));
    },

    getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }
  },
  computed: {
    ...mapState({
      error: state => state.auth.errors
    })
  }
};
</script>
