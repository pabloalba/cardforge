import Vue from "vue"
import Router from "vue-router"
import Home from "@/components/home/Home"
import Login from "@/components/login/Login"
import Game from "@/components/game/Game"
import CardBuilder from "@/components/cardbuilder/CardBuilder"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home
    },
    {
      path: "/login",
      name: "Login",
      component: Login
    },
    {
      path: "/game/:id",
      name: "Game",
      component: Game,
      props: true
    },
    {
      path: "/cardbuilder",
      name: "CardBuilder",
      component: CardBuilder
    }
  ]
})
