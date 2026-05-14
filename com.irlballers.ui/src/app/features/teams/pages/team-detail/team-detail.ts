import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {Team, TeamService} from '../../../../core/services/team/team';
import {CommonModule, NgOptimizedImage} from '@angular/common';
import {ActivatedRoute, RouterLink} from '@angular/router';
import {Player} from '../../../../core/services/player/player';

@Component({
  selector: 'app-team-detail',
  imports: [CommonModule, RouterLink, NgOptimizedImage],
  standalone: true,
  templateUrl: './team-detail.html',
  styleUrl: './team-detail.css',
})
export class TeamDetail implements OnInit {
  team?: Team | null = null;
  roster?: Player[] = [];

  constructor(
    private teamService: TeamService,
    private cdr: ChangeDetectorRef,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    const teamId = Number(this.route.snapshot.paramMap.get('id'));

    this.teamService.getTeamById(teamId).subscribe({
      next: (data) => {
        this.team = data;
        console.log(this.team);
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error fetching team:', error);
      }
    })

    this.teamService.getTeamRoster(teamId).subscribe({
      next: (data) => {
        this.roster = data;
        console.log(this.roster);
        this.cdr.detectChanges();
      }
    })
  }
}
