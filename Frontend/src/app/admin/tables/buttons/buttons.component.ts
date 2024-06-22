import { Component, OnInit } from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {RouterLink, RouterLinkActive, RouterOutlet, Router} from "@angular/router";

@Component({
  selector: 'app-buttons',
  templateUrl: './buttons.component.html',
  styleUrls: ['./buttons.component.css'],
  standalone: true,
  imports: [MatIconModule, MatButtonModule, RouterLink, RouterLinkActive, RouterOutlet]
})
export class ButtonsComponent implements OnInit {

  constructor(router: Router) { }

  ngOnInit() {
  }

}
