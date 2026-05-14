import {ChangeDetectorRef, Component, OnDestroy, OnInit} from '@angular/core';
import {Team, TeamService} from '../../../../core/services/team/team';
import {CommonModule, NgOptimizedImage} from '@angular/common';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-teams-list',
  imports: [CommonModule, RouterLink, NgOptimizedImage],
  standalone: true,
  templateUrl: './teams-list.html',
  styleUrl: './teams-list.css',
})
export class TeamsList implements OnInit {
  instanceId = Math.random();
  teams: Team[] = [];

  constructor(
    private teamService: TeamService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    console.log('INSTANCE:', this.instanceId);
    this.teamService.getTeams().subscribe({
      next: (data) => {
        this.teams = data.results;
        console.log('data.results: ',data.results);
        console.log('teams: ',this.teams);
        console.log('INSTANCE AFTER SET:', this.instanceId, this.teams.length);
        this.cdr.detectChanges(); // force template refresh
      },
      error: (err) => console.error('teams error:', err),

    });
  }

}
