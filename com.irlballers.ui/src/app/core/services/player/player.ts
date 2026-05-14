import { Injectable } from '@angular/core';
import {Team} from '../team/team';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';


export interface Player {
  id: number;
  name: string;
  position: string;
  jersey: number;
  team: Team;
  country: string;
  school: string;
  birthdate: string;
  height: string;
  weight: number;
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
export class PlayerService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor( private http: HttpClient ) { }

  getPlayers(): Observable<PaginatedResponse<Player>> {
    return this.http.get<PaginatedResponse<Player>>(`${this.apiUrl}/players/`);
  }

  getPlayerById(id: number): Observable<Player> {
    return this.http.get<Player>(`${this.apiUrl}/players/${id}/`);
  }

  getPlayerStats(playerId: number) {
    return this.http.get<any>(`${this.apiUrl}/player-stats/${playerId}/`);
  }

}
