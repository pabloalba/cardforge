import Vue from "vue"
import Router from "vue-router"
import Home from "@/components/home/Home"
import Login from "@/components/login/Login"
import Game from "@/components/game/Game"
import Deck from "@/components/deck/Deck"
import CardBuilder from "@/components/cardbuilder/CardBuilder"

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/login",
      name: "login",
      component: Login
    },
    {
      path: "/game/:id",
      name: "game",
      component: Game,
      props: true
    },
    {
      path: "/cardbuilder",
      name: "card-builder",
      component: CardBuilder
    },
    {
      path: "/deck/:id",
      name: "deck",
      component: Deck,
      props: true
    }
  ]
})
