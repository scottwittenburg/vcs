import basevcstest


class TestVCSMarkers2(basevcstest.VCSBaseTest):
    def testVCSMarkers2(self):
        self.x.setcolormap("classic")
        m = self.x.createmarker()

        names = ['dot', 'plus', 'star', 'circle', 'cross', 'diamond', 'triangle_up_fill', 'triangle_down_fill', 'triangle_left', 'triangle_right', 'diamond_fill', 'square_fill', 'hurricane']
        sizes = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]

        m.x = []
        m.y = []
        m.worldcoordinate = []
        m.type = []
        m.color = []
        m.size = []

        for i in range(0, len(names)):
            x = 0
            y = i * 60
            for j in range(0, len(sizes)):
                m.x.append([float(x), ])
                m.y.append([float(y), ])
                x += sizes[j]
                m.size.append(sizes[j])
                m.type.append(names[i])
                m.color.append(242)

        m.worldcoordinate = [-20, 405, -20, 800]

        self.x.plot(m, bg=self.bg)
        self.checkImage("test_vcs_markers_2.png")
