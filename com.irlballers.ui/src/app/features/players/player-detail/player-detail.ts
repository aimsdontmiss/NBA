import {ChangeDetectorRef, Component} from '@angular/core';
import {Player, PlayerService} from '../../../core/services/player/player';
import {TeamService} from '../../../core/services/team/team';
import {ActivatedRoute, RouterLink} from '@angular/router';

@Component({
  selector: 'app-player-detail',
  imports: [RouterLink],
  templateUrl: './player-detail.html',
  styleUrl: './player-detail.css',
})
export class PlayerDetail {
  player?: Player;
  stats?: any;

  constructor(
    private playerService: PlayerService,
    private cdr: ChangeDetectorRef,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    const playerId = Number(this.route.snapshot.paramMap.get('id'));

    this.playerService.getPlayerById(playerId).subscribe({
      next: (data) => {
        this.player = data;
        console.log(this.player);
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error fetching player:', error);
      }
    })

    this.playerService.getPlayerStats(playerId).subscribe({
      next: (data) => {
        this.stats = data;
        console.log(this.stats);
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error fetching player stats:', error);
      }
    })
  }
}
