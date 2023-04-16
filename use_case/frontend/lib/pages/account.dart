import 'package:flutter/material.dart';

class PageAccount extends StatelessWidget {
  int _selectedIndex = 1;

  /*void _changeAccountTab(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }*/

  final List<Widget> _accountTabs = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Column(
      children: [
        Container(
          height: 240,
          color: Colors.white,
        ),
        Positioned(
          top: 240,
          left: 0,
          right: 0,
          child: DefaultTabController(
            length: 3,
            child: Scaffold(
              body: Column(
                children: [
                  const TabBar(tabs: [
                    Tab(
                      text: "Friends",
                    ),
                    Tab(
                      text: "Close Friends",
                    ),
                    Tab(
                      text: "Requests",
                    ),
                  ]),
                  SizedBox(
                    height: MediaQuery.of(context).size.height - 240,
                    width: MediaQuery.of(context).size.width,
                    child: TabBarView(
                      children: [
                        //1
                        Container(
                          child: Center(
                            child: Text('1st Tab'),
                          ),
                        ),
                        //2
                        Container(
                          child: Center(
                            child: Text('1st Tab'),
                          ),
                        ),
                        //3
                        Container(
                          child: Center(
                            child: Text('1st Tab'),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    ));
  }
}
