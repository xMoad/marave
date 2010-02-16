%Module SyntaxHighlighter 0

%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip


%ModuleHeaderCode
#include <srchiliteqt/Qt4SyntaxHighlighter.h>
%End

namespace srchiliteqt {

class Qt4SyntaxHighlighter { 
%TypeHeaderCode
#include <srchiliteqt/Qt4SyntaxHighlighter.h>
%End

public:
    Qt4SyntaxHighlighter(QTextDocument *doc = 0);
    void init(const QString &langFile, const QString &styleFile=
            "default.style");
    bool initFromFileName(const QString &fileName);

private:
   Qt4SyntaxHighlighter(const srchiliteqt::Qt4SyntaxHighlighter&);

};

};
