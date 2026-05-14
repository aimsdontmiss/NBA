import { Routes } from '@angular/router';
import {TeamsList} from './features/teams/pages/teams-list/teams-list';
import {TeamDetail} from './features/teams/pages/team-detail/team-detail';
import {PlayerDetail} from './features/players/player-detail/player-detail';

export const routes: Routes = [
  { path: '', redirectTo: 'teams', pathMatch: 'full' },
  { path: 'teams', component: TeamsList },
  { path: 'teams/:id', component: TeamDetail },
  { path: 'players/:id', component: PlayerDetail },


  { path: '**', redirectTo: 'teams' },

];
