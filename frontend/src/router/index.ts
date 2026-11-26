import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Humanizer from '../views/Humanizer.vue'
import Detector from '../views/Detector.vue'
import Rewriter from '../views/Rewriter.vue'
import Paraphraser from '../views/Paraphraser.vue'
import EssayRewriter from '../views/EssayRewriter.vue'
import ArticleRewriter from '../views/ArticleRewriter.vue'
import SentenceRewriter from '../views/SentenceRewriter.vue'
import ParagraphRewriter from '../views/ParagraphRewriter.vue'
import ContentImprovement from '../views/ContentImprovement.vue'
import Grammar from '../views/Grammar.vue'
import Workspace from '../views/Workspace.vue'
import Login from '../views/Login.vue'
import NotFound from '../views/NotFound.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/humanizer', name: 'humanizer', component: Humanizer },
    { path: '/detector', name: 'detector', component: Detector },
    { path: '/rewriter', name: 'rewriter', component: Rewriter },
    { path: '/paraphraser', name: 'paraphraser', component: Paraphraser },
    { path: '/essay-rewriter', name: 'essay-rewriter', component: EssayRewriter },
    { path: '/article-rewriter', name: 'article-rewriter', component: ArticleRewriter },
    { path: '/sentence-rewriter', name: 'sentence-rewriter', component: SentenceRewriter },
    { path: '/paragraph-rewriter', name: 'paragraph-rewriter', component: ParagraphRewriter },
    { path: '/content-improvement', name: 'content-improvement', component: ContentImprovement },
    { path: '/grammar', name: 'grammar', component: Grammar },
    { path: '/workspace', name: 'workspace', component: Workspace },
    { path: '/login', name: 'login', component: Login },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFound },
  ],
})

export default router
