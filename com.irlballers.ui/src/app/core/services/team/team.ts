import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type {Player} from '../player/player';


export interface Team {
  id: number;
  name: string;
  abbr: string;

}

export type PaginatedResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};

@Injectable({
  providedIn: 'root',
})
export class TeamService {
  private apiUrl = 'http://127.0.0.1:8000/api/teams/';

  constructor( private http: HttpClient ) { }

  getTeams(): Observable<PaginatedResponse<Team>> {
    return this.http.get<PaginatedResponse<Team>>(this.apiUrl);
  }

  getTeamById(id: number): Observable<Team> {
    return this.http.get<Team>(`${this.apiUrl}${id}/`);
  }

  getTeamRoster(teamId: number) {
    return this.http.get<Player[]>(`${this.apiUrl}${teamId}/roster/`);
  }
}
