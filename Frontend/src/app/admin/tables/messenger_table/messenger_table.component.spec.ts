import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Messenger_tableComponent } from './messenger_table.component';

describe('MessengerTableComponent', () => {
  let component: Messenger_tableComponent;
  let fixture: ComponentFixture<Messenger_tableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Messenger_tableComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Messenger_tableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
